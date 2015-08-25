import socket, memory
import constants

class Client:

    def __init__(self, player):
        self.player = player
        color = self.player.getColor()
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if   color == 'W': tcpPort = constants.TCP_PORT_1
        elif color == 'B': tcpPort = constants.TCP_PORT_2
        else: assert False, "ERROR: expect color to be 'W' or 'B'"
        self.soc.connect((constants.TCP_IP, tcpPort))

    def run(self):
        data = self.player.getColor()
        assert data == 'W' or data == 'B', "ERROR: expecting color to be 'W' or 'B'"
        self.soc.send(data)

        while True:
            data = self.soc.recv(constants.BUF_SIZE)
            choice = int(data[0])
            data = data[1:]
            outData = None
            if choice == 1: #chooseMove
                board = self.unpackBoard(data)
                a = constants.BRD_SIZE*constants.BRD_SIZE                
                data = data[a:]
                cols = data.strip().split()
                prevMove = int(cols[0]),  int(cols[1])
                
                if prevMove[0] >= constants.BRD_SIZE or prevMove[1] >=constants.BRD_SIZE : prevMove = None
                move = self.player.chooseMove(board, prevMove)
                memMB = memory.getMemoryUsedMB()
                if move:  outData = '%d %d %f' % (move[0], move[1], memMB)
                else:     outData = '%d %d %f' % (constants.BRD_SIZE+1, constants.BRD_SIZE+1, memMB) #no move                
                self.soc.send(outData)

            elif choice == 2: #gameEnd
                board = self.unpackBoard(data)
                self.player.gameEnd(board)
                outData = '0' #noop
                self.soc.send(outData)
                break
            else:
                assert False, 'ERROR: expect data[0] to be 0 or 1'

        self.soc.close()

    def unpackBoard(self, data):
        board = [[None for i in xrange(constants.BRD_SIZE)] for j in xrange(constants.BRD_SIZE)]
        for a in xrange(constants.BRD_SIZE*constants.BRD_SIZE):
            i, j = divmod(a, constants.BRD_SIZE)
            board[i][j] = data[a]
        return board
