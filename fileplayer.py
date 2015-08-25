class FilePlayer:

    def __init__(self, color, fileName):
        '''
        Make sure to store the color of your player ('B' or 'W')
        You may init your data structures here, if any
        '''
        self.color = color #color is 'B' or 'W'
        self.idx = 0
        self.moves = []

        fin = open(fileName)
        lines = fin.readlines()
        fin.close()
        for line in lines:
            line = line.strip()
            if len(line) <= 0: continue
            cols = line.split()
            if cols[0].startswith('%s:' % self.color):
                i = int(cols[1])
                j = int(cols[2])
                if i < 0 or j < 0: self.moves.append( None )
                else:              self.moves.append( (i,j) )

    def chooseMove(self, board, prevMove):
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
        if self.idx < len(self.moves):
            m =  self.moves[self.idx]
            self.idx += 1
            return m
        return None

    def gameEnd(self, board):
        '''
        This is called when the game has ended.
        Add clean-up code here, if necessary.
        board is a copy of the end-game board configuration.
        '''
        pass

    def getColor(self):
        '''
        Returns the color of the player
        '''
        return self.color

    def getMemoryUsedMB(self):
        return 0.0
