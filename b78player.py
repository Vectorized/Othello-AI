import random, memory, constants
from b78 import *

class Player:

    def __init__(self, color):
        self.color = color.upper()

        self.whiteStartFirst = -1

        # For AI competition
        competitionSchedule = {
            "midGameTimeLeft"    : 60 * 18, 
            "gameTimeLeft"       : 60 * 25,
            "minSearchDepth"     : 6  ,
            "endGameNumEmpties"  : 14 }

        # Used to challenge on:
        # https://www.flyordie.com/reversi/ 
        flyOrDieSchedule = {
            "midGameTimeLeft"    : 60 * 0.5, 
            "gameTimeLeft"       : 60 * 1.8,
            "minSearchDepth"     : 6  ,
            "endGameNumEmpties"  : 14 }

        # For testing endgame speed
        endGameFanaticSchedule = {
            "midGameTimeLeft"    : 30 * 1, 
            "gameTimeLeft"       : 60 * 10,
            "minSearchDepth"     : 4  ,
            "endGameNumEmpties"  : 14 }

        self.schedule = flyOrDieSchedule
        
        self.schedule["previousDepthCounters"] = None
        self.schedule["previousSearchTime"]    = None

        self.printBoard = True

    def chooseMove(self, board, prevMove):
        functionStartTime = time.time()

        '''
        board is a two-dimensional list representing the current board configuration.
        board is a copy of the original game board, so you can do to it as you wish.
        board[i][j] is 'W', 'B', 'G' when row i and column j contains a
        white piece, black piece, or no piece respectively.
        As usual i, j starts from 0, and board[0][0] is the top-left corner.
        prevMove gives the i, j coordinates of the last move made by your opponent.
        prevMove[0] and prevMove[1] are the i and j-coordinates respectively.
        prevMove may be None if your opponent has no move to make during his last turn.
        '''       
        player, opponent = makeBitBoard(board, self.color)
        numEmptiesLeft = getNumEmptiesLeft(player, opponent)

        # Check if the engine unconventionally asks white to play first.
        # If yes, we flip horizontally for the game.
        if self.whiteStartFirst == -1:
            if numEmptiesLeft == 60:
                self.whiteStartFirst = self.color == 'W'
            elif numEmptiesLeft == 59:
                self.whiteStartFirst = self.color == 'B'
            if self.whiteStartFirst:
                print "White Starts First!"
            else:
                print "Black Starts First!"

        if self.whiteStartFirst:
            player = horizontalMirrorDiscsSingle(player)
            opponent = horizontalMirrorDiscsSingle(opponent)

        moveMade = False
        useOpeningBook = True
        validMoves = getMoves(player, opponent)
        score = "N.A."

        if validMoves:

            if useOpeningBook: # If opening book is to be used
                combined = (player << 128) | opponent
                unique, symmetryIndex = getUniqueBoard(combined) # Not rly a perf issue... only ~ 30x per game
                if unique in openingBook:
                    move = getSymmetricMoveSingleInverse(random.choice(openingBook[unique]), symmetryIndex)
                    moveMade = True
                    print "Opening book used!"

            if not moveMade:
                searchDepth = getSuggestedDepthForCompetition(
                    self.schedule["midGameTimeLeft"], 
                    self.schedule["gameTimeLeft"],
                    self.schedule["endGameNumEmpties"], 
                    self.schedule["minSearchDepth"],
                    player, 
                    opponent,
                    self.schedule["previousDepthCounters"], 
                    self.schedule["previousSearchTime"])
                isEndGame = searchDepth > 60
                if isEndGame:
                    print "Endgame Search, # Empties:", numEmptiesLeft
                else:
                    print "Search Depth:", searchDepth
                # init schedule analysis stuff
                depthCounters = None if isEndGame else getNewDepthCounters(searchDepth) 
                searchTimeStart = time.time()
                # do search
                searchResults = reversiABNegaScout(player, opponent, searchDepth, depthCounters)
                # record schedule analysis stuff
                searchTime = time.time() - searchTimeStart
                self.schedule["previousDepthCounters"] = depthCounters
                self.schedule["previousSearchTime"] = searchTime
                # assign search results
                move, score = searchResults
                moveMade = True
        else:
            return None # No valid move, better return None

        if self.printBoard:
            try:
                rev = [m[1] for m in validMoves if m[0] == move][0]
                printPlayer, printOpponent = getPut(player, opponent, move, rev)
                if self.whiteStartFirst:
                    printPlayer = horizontalMirrorDiscsSingle(printPlayer)
                    printOpponent = horizontalMirrorDiscsSingle(printOpponent)
                printBitBoard(printPlayer, printOpponent, self.color)
            except:
                pass

        # Print stats...
        ramUsage = ""
        try:
            ramUsage = " RAM: %2.1fMB" % memory.getMemoryUsedMB()
        except:
            pass
        printLines = (
            "Move: " + bitToLetterCoors[move] + " Score: " + str(score),
            "Time Left: %ds" % (self.schedule["gameTimeLeft"] - (time.time() - functionStartTime)) + ramUsage )
        print "\n".join(printLines)
        print "=" * max(len(l) for l in printLines) + "\n"

        # Flip back move if needed...
        if self.whiteStartFirst:
            move = bitToIndex2D[horizontalMirrorDiscsSingle(move)]
        else:
            move = bitToIndex2D[move]

        functionTime = time.time() - functionStartTime
        self.schedule["midGameTimeLeft"] -= functionTime
        self.schedule["gameTimeLeft"] -= functionTime

        return move

    def gameEnd(self, board):
        '''
        This is called when the game has ended.
        Add clean-up code here, if necessary.
        board is a copy of the end-game board configuration.
        '''
        # no clean up necessary for random player
        pass

    def getColor(self):
        '''
        Returns the color of the player
        '''
        return self.color
    
    def getMemoryUsedMB(self):
        '''
        You do not need to add to this code. Simply have it return 0
        '''
        return 0.0

    ########################### SUPPORT CODE #############################

    def validMove(self, board, pos, ddir, color, oppColor):
        newPos = (pos[0]+ddir[0], pos[1]+ddir[1])
        validPos = newPos[0] >= 0 and newPos[0] < constants.BRD_SIZE and newPos[1] >= 0 and newPos[1] < constants.BRD_SIZE
        if not validPos: return False
        if board[newPos[0]][newPos[1]] != oppColor: return False

        while board[newPos[0]][newPos[1]] == oppColor:
            newPos = (newPos[0]+ddir[0], newPos[1]+ddir[1])
            validPos = newPos[0] >= 0 and newPos[0] < constants.BRD_SIZE and newPos[1] >= 0 and newPos[1] < constants.BRD_SIZE
            if not validPos: break

        validPos = newPos[0] >= 0 and newPos[0] < constants.BRD_SIZE and newPos[1] >= 0 and newPos[1] < constants.BRD_SIZE
        if validPos and board[newPos[0]][newPos[1]] == color:
            return True
        return False
