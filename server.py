import socket
import constants

class Server:

    def __init__(self, serverNum):
        assert serverNum == 1 or serverNum == 2, 'Expecting 1 or 2 as severNum'
        self.serverNum = serverNum
        self.memUsedMB = 0.0

        self.soc = socket.socket()
        if   serverNum == 1: tcpPort = constants.TCP_PORT_1
        else:                tcpPort = constants.TCP_PORT_2
        self.soc.bind((constants.TCP_IP, tcpPort))
        self.soc.listen(5)
        self.conn, addr = self.soc.accept()
        print ('server %d connected with ' % serverNum),  addr

        data = self.conn.recv(constants.BUF_SIZE)
        self.color = data[0]
        assert self.color == 'W' or self.color == 'B', "ERROR: expect 'W' or 'B'"
        assert (self.color == 'W' and self.serverNum == 1) or \
               (self.color == 'B' and self.serverNum == 2)

    def chooseMove(self, boardCopy, prevMove):
        data = [None] * (1+constants.BRD_SIZE * constants.BRD_SIZE+2)
        data[0] = '1' # chooseMove
        self.packBoard(boardCopy, data)
        if prevMove:
            data[-2] = '%d ' % prevMove[0]
            data[-1] = '%d ' % prevMove[1]
        else:
            data[-2] = '%d ' % (constants.BRD_SIZE + 1)
            data[-1] = '%d ' % (constants.BRD_SIZE + 1)

        data = ''.join(data)
        self.conn.send(data)
        data = self.conn.recv(constants.BUF_SIZE)
        cols = data.strip().split()
        x = int(cols[0])
        y = int(cols[1])
        self.memUsedMB = float(cols[2])
        #idx = data.rfind(' ')
        #self.memUsedMB = float(data[idx+1:])   
        if x >= constants.BRD_SIZE or y >= constants.BRD_SIZE: return None
        return x, y

    def gameEnd(self, boardCopy):
        data = [None] * (1+constants.BRD_SIZE * constants.BRD_SIZE)
        data[0] = '2' #gameEnd
        self.packBoard(boardCopy, data)
        data = ''.join(data)
        self.conn.send(data)
        data = self.conn.recv(constants.BUF_SIZE)
        self.conn.close()
        self.soc.close()

    def getColor(self):
        return self.color

    def getMemoryUsedMB(self):
        return self.memUsedMB

    def packBoard(self, boardCopy, data):
        idx = 1
        for i in xrange(constants.BRD_SIZE):
            for j in xrange(constants.BRD_SIZE):
                data[idx] = boardCopy[i][j]
                idx += 1

