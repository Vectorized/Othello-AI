import Tkinter, time, copy, datetime
import constants

class Board:

    def __init__(self):
        self.moveXY   = None
        self.moveMade = False
        self.curPlayer = 'W'
        self.dirs = copy.copy(constants.DIRECTIONS)

        self.board = [None] * constants.BRD_SIZE
        for i in xrange(constants.BRD_SIZE):
            self.board[i] = ['G'] * constants.BRD_SIZE
       
        b = int(constants.BRD_SIZE / 2)
        a = b-1    
        self.board[a][a] = 'W'
        self.board[b][b] = 'W'
        self.board[a][b] = 'B'
        self.board[b][a] = 'B'

        self.flipBoxes = []
        self.createGUI()
        self.on = True

    def __str__(self):
        sstr = ''
        for i in xrange(constants.BRD_SIZE):
            for j in xrange(constants.BRD_SIZE):
                if   self.board[i][j] == 'W': sstr += 'W '
                elif self.board[i][j] == 'B': sstr += 'B '
                elif self.board[i][j] == 'G': sstr += '_ '
                else: assert False, 'board is not W, B or G'
            sstr += "\n"
        sstr += self.curPlayer + '\n'
        return sstr

    def curPlayerColorStr(self):
        if self.curPlayer == 'W': return 'White'
        if self.curPlayer == 'B': return 'Black'
        return 'Error: no curPlayer'


    ################################### GUI ####################################

    def createGUI(self):
        self.guiOn     = True
        self.guiTk     = Tkinter.Tk()
        self.guiCanvas = Tkinter.Canvas(self.guiTk, bg=constants.BRD_COLOR, height=constants.BRD_HW, width=constants.BRD_HW)
        self.guiMsg    = Tkinter.StringVar()
        self.curBox    = self.guiCanvas.create_rectangle(0, 0,
                                                         constants.CELL_HW*constants.BRD_SIZE,
                                                         constants.CELL_HW*constants.BRD_SIZE,
                                                         outline=constants.CURBOX_COLOR,
                                                         width=constants.CURBOX_BORDER)
        Tkinter.Label(self.guiTk, textvariable=self.guiMsg, font=(constants.FONT_TYPE, constants.FONT_SIZE)).pack()
        self.guiTk.protocol('WM_DELETE_WINDOW', self.guiExit) #callback to exit game
        self.guiCanvas.bind('<Button-1>', self.guiClick)      #callback for mouse click

        self.guiBoard = [None] * constants.BRD_SIZE
        for i in range(constants.BRD_SIZE):
            self.guiBoard[i] = [None] * constants.BRD_SIZE

        for i in xrange(1,constants.BRD_SIZE):
            self.guiCanvas.create_line(0, i*constants.CELL_HW, constants.BRD_HW, i*constants.CELL_HW) #draw horizontal line
            self.guiCanvas.create_line(i*constants.CELL_HW, 0, i*constants.CELL_HW, constants.BRD_HW) #draw vertical line

        self.guiCanvas.pack()
        self.guiCanvas.focus_set()
        self.guiTk.update()

    def guiExit(self):
        self.on = False
        self.guiTk.destroy()

    def guiClick(self, event):
        self.moveXY   = (event.y/constants.CELL_HW, event.x/constants.CELL_HW)
        self.moveMade = True

    def guiDrawBoard(self, curMove, flips):
        for i in range(constants.BRD_SIZE):
            for j in range(constants.BRD_SIZE):
                color = self.board[i][j]
                if   color == 'B': cellColor = 'black'
                elif color == 'W': cellColor = 'white'
                else:
                    self.guiBoard[i][j] = None
                    continue

                if self.guiBoard[i][j] == None:
                    self.guiBoard[i][j] = self.guiMakePiece(i,j,cellColor)
                else:
                    self.guiCanvas.itemconfig(self.guiBoard[i][j],fill=cellColor)

        if curMove:
            self.guiCanvas.coords(self.curBox,
                                  curMove[1]*constants.CELL_HW+1,
                                  curMove[0]*constants.CELL_HW+1,
                                  (curMove[1]+1)*constants.CELL_HW-1,
                                  (curMove[0]+1)*constants.CELL_HW-1)
        else:
            self.guiCanvas.coords(self.curBox,0,0,0,0)

        if flips:
            for box in self.flipBoxes:
                self.guiCanvas.delete(box)
            self.flipBoxes = []

            for flip in flips:
                box = self.guiCanvas.create_rectangle(0, 0, 0, 0,
                                                      outline=constants.FLIP_COLOR,
                                                      width=constants.FLIP_BORDER)
                self.guiCanvas.coords(box,
                                      flip[1]*constants.CELL_HW+1,
                                      flip[0]*constants.CELL_HW+1,
                                      (flip[1]+1)*constants.CELL_HW-1,
                                      (flip[0]+1)*constants.CELL_HW-1)
                self.flipBoxes.append(box)

    def guiMakePiece(self, i, j, color):
        return self.guiCanvas.create_oval(    j*constants.CELL_HW+2,     i*constants.CELL_HW+2,
                                          (j+1)*constants.CELL_HW-2, (i+1)*constants.CELL_HW-2,
                                          fill=color)

    ############################### GAME LOGIC #################################

    @staticmethod
    def addToPos(pos,ddir):
        return (pos[0]+ddir[0], pos[1]+ddir[1])

    @staticmethod
    def validPos(pos):
        return pos[0] >= 0 and pos[0] < constants.BRD_SIZE and \
               pos[1] >= 0 and pos[1] < constants.BRD_SIZE

    @staticmethod
    def oppositeColor(color):
        if color == 'W': return 'B'
        if color == 'B': return 'W'
        assert False, 'Color is neither W or B'

    @staticmethod
    def getTime():
        return time.time() #use this for wall-clock time across OSes
        #return time.clock()

    def computeScore(self):
        w = b = 0
        for i in range(constants.BRD_SIZE):
            for j in range(constants.BRD_SIZE):
                color = self.board[i][j]
                if   color == 'W': w += 1
                elif color == 'B': b += 1
        return w, b

    def hasMove(self, color):
        oppColor = Board.oppositeColor(color)
        moves = self.findAllMovesHelper(color, oppColor, checkHasMoveOnly=True)
        return len(moves) > 0

    def isEndGame(self):
        for color, oppColor in (('B','W'), ('W','B')):
            moves = self.findAllMovesHelper(color, oppColor, checkHasMoveOnly=True)
            if len(moves) > 0: return False
        return True

    def findAllMoves(self):
        color = self.curPlayer
        oppColor = Board.oppositeColor(color)
        return self.findAllMovesHelper(color, oppColor)

    def findAllMovesHelper(self, color, oppColor, checkHasMoveOnly=False):
        moves = []
        for i in xrange(constants.BRD_SIZE):
            for j in xrange(constants.BRD_SIZE):
                if self.board[i][j] != 'G': continue
                for ddir in self.dirs:
                    if self.validMove((i,j), ddir, color, oppColor):
                        moves.append((i,j))
                        if checkHasMoveOnly: return moves
                        break
        return moves

    def makeMove(self, pos):
        flips = []
        if pos == None: return flips
        color = self.curPlayer
        self.board[pos[0]][pos[1]] = color
        oppColor = Board.oppositeColor(color)

        for ddir in self.dirs:
            if self.validMove(pos, ddir, color, oppColor):
                newPos = Board.addToPos(pos, ddir)
                while self.board[newPos[0]][newPos[1]] == oppColor:
                    self.board[newPos[0]][newPos[1]] = color
                    flips.append(newPos)
                    newPos = Board.addToPos(newPos, ddir)
        return flips

    def validMove(self, pos, ddir, color, oppColor):
        newPos = Board.addToPos(pos, ddir)
        if not Board.validPos(newPos):                   return False
        if self.board[newPos[0]][newPos[1]] != oppColor: return False

        while self.board[newPos[0]][newPos[1]] == oppColor:
            newPos = Board.addToPos(newPos, ddir)
            if not Board.validPos(newPos): break

        if Board.validPos(newPos) and self.board[newPos[0]][newPos[1]] == color:
            return True
        return False

    def validMoveInSomeDir(self, pos, color, oppColor):
        for ddir in self.dirs:
            if self.validMove(pos, ddir, color, oppColor):
                return True
        return False

    def playGame(self, white, black):
        whiteSec   = 0.0
        blackSec   = 0.0
        whiteMoves = 0
        blackMoves = 0
        prevMove   = None
        numNoneMoves = 0
        self.curPlayer = constants.FIRST_PLAYER
        message = ''
        timeExceeded = False
        memExceeded  = False
        log = open(datetime.datetime.now().strftime("gamelog-%Y-%m-%d_%H-%M-%S.txt"), 'w')

        self.guiDrawBoard(None, None)
        self.guiTk.configure(cursor='watch')
        self.guiTk.update()

        while not self.isEndGame():
            boardCopy = copy.deepcopy(self.board)
            timeExceeded = False
            memExceeded  = False
                       
            if self.curPlayer == 'W': player , timeSec = white, whiteSec
            else:                     player , timeSec = black, blackSec
            memUsedMB = player.getMemoryUsedMB()

            if timeSec   > constants.TIME_LIMIT_SEC:  timeExceeded = True
            if memUsedMB > constants.MEMORY_LIMIT_MB: memExceeded  = True 

            diffSec = 0.0           
            if not timeExceeded and not memExceeded and self.hasMove(player.getColor()):
                startSec = Board.getTime() 
                move = player.chooseMove(boardCopy, prevMove)                     
                diffSec = Board.getTime() - startSec
            else: 
                move = None

            if move == None:
                numNoneMoves += 1
                if numNoneMoves == 2:
                    whiteExceedTime = whiteSec > constants.TIME_LIMIT_SEC
                    blackExceedTime = blackSec > constants.TIME_LIMIT_SEC
                    whiteMem = white.getMemoryUsedMB()
                    blackMem = black.getMemoryUsedMB()
                    whiteExceedMem  = whiteMem > constants.MEMORY_LIMIT_MB
                    blackExceedMem  = blackMem > constants.MEMORY_LIMIT_MB 
                    message = 'No moves for two consecutive plies.\n'
                    if whiteExceedTime: message += 'White exceeded time limit!\n'
                    if blackExceedTime: message += 'Black exceeded time limit!\n'
                    if whiteExceedMem:  message += 'White exceeded memory limit!\n'
                    if blackExceedMem:  message += 'Black exceeded memory limit!\n'
                    log.write('M: Both players have no valid moves\n')
                    log.write('M: W exceeded time = %d (%f secs); B exceeded time = %d (%f secs)\n' % \
                              (int(whiteExceedTime), whiteSec, int(blackExceedTime), blackSec)  )
                    log.write('M: W exceeded mem  = %d (%f MB); B exceeded time = %d (%f MB)\n' %  \
                              (int(whiteExceedMem), whiteMem, int(blackExceedMem), blackMem) )
                    break
            else:
                numNoneMoves = 0

            prevMove = move

            if self.curPlayer == 'W':
                whiteSec += diffSec
                if move: whiteMoves += 1
            else:
                blackSec += diffSec
                if move: blackMoves += 1

            if move != None and not self.validMoveInSomeDir(move, self.curPlayer, Board.oppositeColor(self.curPlayer)):
                message = '%s has provided an invalid move %s! Terminating...\n' % (self.curPlayerColorStr(), move)
                log.write('M: ' + message)
                break

            flips = self.makeMove(move)

            if move == None:
                if self.curPlayer == 'W': timeSec, memMB = whiteSec, white.getMemoryUsedMB()
                else:                     timeSec, memMB = blackSec, black.getMemoryUsedMB()
                msg = '%s has no moves. ' % self.curPlayerColorStr()
                log.write('%s: -1 -1' % self.curPlayer)
                if timeExceeded:
                    msg += '\n%s EXCEEDED TIME LIMIT! (%f secs).\n' % (self.curPlayerColorStr(), timeSec)
                    log.write(' ; time exceeded (%f secs)' % timeSec)
                if memExceeded:
                    msg += '%s EXCEEDED MEMORY LIMIT! (%f MB).\n' % (self.curPlayerColorStr(), memMB)
                    log.write(' ; memory exceeded (%f MB)' % memMB) 
                log.write('\n')
            else:
                msg = ''
                log.write('%s: %d %d\n' % (self.curPlayer, move[0], move[1]))

            wpieces, bpieces = self.computeScore()
            self.curPlayer = self.oppositeColor(self.curPlayer)
            msg += "(W: %d , B: %d).  %s's turn..." % (wpieces, bpieces, self.curPlayerColorStr())
            self.guiMsg.set(msg )
            self.guiDrawBoard(move, flips)
            self.guiTk.configure(cursor='watch')
            self.guiTk.update()
            time.sleep(constants.MOVE_SEC)

        boardCopy = copy.deepcopy(self.board)
        white.gameEnd(boardCopy)
        black.gameEnd(boardCopy)

        whiteMB = white.getMemoryUsedMB()
        blackMB = black.getMemoryUsedMB()

        wscore, bscore = self.computeScore()
        message += 'White: %d  Moves: %d  MB: %f  Secs: %f\n' % \
                    (wscore, whiteMoves, whiteMB, whiteSec)
        message += 'Black: %d  Moves: %d  MB: %f  Secs: %f\n' % \
                   (bscore, blackMoves, blackMB, blackSec)
        
        whiteSec = round(whiteSec,1)
        blackSec = round(blackSec,1)
        whiteMB  = round(whiteMB, 1)
        blackMB  = round(blackMB, 1)
                   
        if   wscore > bscore:     message += 'White wins!\n'
        elif wscore < bscore:     message += 'Black wins!\n'
        elif whiteSec < blackSec: message += 'White wins (by using less time)!\n'
        elif whiteSec > blackSec: message += 'Black wins (by using less time)!\n'
        elif whiteMB  < blackMB:  message += 'White wins (by using less memory)!\n'
        elif whiteMB  > blackMB:  message += 'Black wins (by using less memory)!\n'
        else:                     message += "It's a draw!\n"
        self.guiMsg.set(message)
        self.guiTk.configure(cursor="X_cursor")

        for box in self.flipBoxes:
            self.guiCanvas.delete(box)
        self.flipBoxes = []

        log.write('M: GAME ENDS\n'+message+'\n')
        log.close()

        while self.on:
            self.guiTk.update()
            time.sleep(constants.SLEEP_SEC)

    ######################### HUMAN PLAYER ####################################

    def chooseMove(self, boardCopy, prevMove):
        '''
        Modeling a human player. Takes inputs from mouse click on board
        '''
        for box in self.flipBoxes:
            self.guiCanvas.delete(box)
        self.flipBoxes = []

        self.moveXY = None
        while self.on:
            self.moveMade = False
            self.guiDrawBoard(None, None)
            self.guiCanvas.focus_force()
            self.guiTk.configure(cursor='target')

            while self.on and not self.moveMade:
                self.guiTk.update()
                time.sleep(constants.SLEEP_SEC)

            if not self.on: break
            assert self.moveMade, 'ERROR: moveMade should be True'

            allMoves = self.findAllMoves()
            if self.moveXY not in allMoves:
                self.guiTk.bell()
                continue

            return self.moveXY

        return self.moveXY

    def gameEnd(self, boardCopy):
        '''
        Modeling a human player. No clean up to do, so simply return.
        '''
        pass
    
    def getColor(self):
        return self.curPlayer

    def getMemoryUsedMB(self):
        return 0.0

if __name__ == '__main__':
    board = Board()

    #two human players using mouse clicks
    #white = board
    #black = board

    #two automated players using random move
    import randomplayer
    white = randomplayer.RandomPlayer('W')
    black = randomplayer.RandomPlayer('B')

    #white: human player, black: player using random move
    #import randomplayer
    #white = board
    #black = randomplayer.RandomPlayer('B')

    #white: player using random move, black: human player
    #import randomplayer
    #white = randomplayer.RandomPlayer('W')
    #black = board

    #two automated players connecting via TCP/IP
    #import server
    #white = server.Server(1)
    #black = server.Server(2)

    #play from log file
    #import fileplayer
    #logFile = 'gamelog-2015-06-06_20-40-29.txt'
    #white = fileplayer.FilePlayer('W', logFile)
    #black = fileplayer.FilePlayer('B', logFile)

    board.playGame(white, black)






