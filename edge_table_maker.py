letterCoors = []
for i in "12345678":
	for a in "ABCDEFGH":
		letterCoors.append(a+i)

EMPTY = 0
BLACK = 1
WHITE = 2

edgeTable = [0] * int(3**10)

topEdge = ("B2", "A1", "B1", "C1", "D1", "E1", "F1", "G1", "H1", "G2")
topEdgeWithoutXs = topEdge[1:-1]
topEdgeBits = {"A1":128, "B1":64, "C1":32, "D1":16, "E1":8, "F1":4, "G1":2, "H1":1}

staticEdgeTable = ((None,    0, -2000),
                   (700,  None,  None),
                   (1200,  200,   -25),
                   (1000,  200,    75),
                   (1000,  200,    50),
                   (1000,  200,    50),
                   (1000,  200,    75),
                   (1200,  200,   -25),
                   (700,  None,  None),
                   (None,    0, -2000))

edgeStaticProbability = ((.10,  .40,  .70),
                         (.05,  .30, None),
                         (.01, None, None))

def getInitialBoard():
	return {sq:EMPTY for sq in topEdge}

def isLegal(player, board, sq):
	playerBits, opponentBits = 0, 0
	opponent = getOpponent(player)
	for e in topEdgeWithoutXs:
		playerBits <<= 1
		opponentBits <<= 1
		if board[e] == player:
			playerBits |= 1
		elif board[e] == opponent:
			opponentBits |= 1
	# print bin(256|playerBits)[3:], bin(256|opponentBits)[3:]
	blankBits = ~ (playerBits | opponentBits)
	# Get left moves
	w = opponentBits & 0x7e
	t = w & (playerBits >> 1)
	t |= w & (t >> 1); t |= w & (t >> 1); t |= w & (t >> 1); t |= w & (t >> 1); t |= w & (t >> 1)
	r = (t >> 1)
	# Get right moves
	t = w & (playerBits << 1)
	t |= w & (t << 1); t |= w & (t << 1); t |= w & (t << 1); t |= w & (t << 1); t |= w & (t << 1)
	r |= (t << 1)
	# print bin(256|r)[3:]
	# print bin(256|topEdgeBits[sq])[3:]
	# for x in topEdgeWithoutXs:
	# 	print bin(256|topEdgeBits[x])[3:]
	return topEdgeBits[sq] & r & blankBits

def edgeIndex(player, board, squares):
	index = 0
	for s in squares:
		index = 3 * index
		if board[s] == EMPTY:
			index += 0
		elif board[s] == player:
			index += 1
		else:
			index += 2
	return index

xSquares = ('B2', 'B7', 'G2', 'G7')
def isXSquare(sq):
	return sq in xSquares

cornerSquares = ('A1', 'A8', 'H1', 'H8')
def isCornerSquare(sq):
	return sq in cornerSquares

xSquareForCornerSquare = dict(zip(cornerSquares, xSquares))
cornerSquareForXSquare = dict(zip(xSquares, cornerSquares))
topNeighbors = {a:[b for b in topEdgeWithoutXs if 
	abs(topEdgeWithoutXs.index(a)-topEdgeWithoutXs.index(b)) == 1] 
	for a in topEdgeWithoutXs}

def countEdgeNeighbors(player, board, sq):
	return sum(board[n] == player for n in topNeighbors[sq])

def edgeMoveProbability(player, board, sq):
	if isXSquare(sq):
		return 0.5
	elif isLegal(player, board, sq):
		return 1.0
	elif isCornerSquare(sq):
		xSquare = xSquareForCornerSquare[sq]
		if board[xSquare] == EMPTY:
			return 0.1
		elif board[xSquare] == player:
			return 0.001
		else:
			return 0.9
	else:
		chancesCoefficient = 2.0 if isLegal(getOpponent(player), board, sq) else 1.0
		return edgeStaticProbability\
			[countEdgeNeighbors(player, board, sq)]\
			[countEdgeNeighbors(getOpponent(player), board, sq)] / chancesCoefficient

def getOpponent(player):
	return BLACK if player == WHITE else WHITE

def edgeStability(player, board):
	return sum(edgeTable[edgeIndex(player, board, edge)] for edge in edgeAndXLists)

def setf(index, value):
	global edgeTable
	edgeTable[index] = value

def possibleEdgeMove(player, board, sq):
	prob = edgeMoveProbability(player, board, sq)
	oriSqVal = board[sq]
	board[sq] = player
	val = -edgeTable[edgeIndex(getOpponent(player), board, topEdge)]
	board[sq] = oriSqVal
	return prob, val

def combineEdgeMoves(possibilities, player):
	prob = 1.0
	val = 0.0
	for pair in sorted(possibilities, key = lambda a:a[1], reverse = player == BLACK):
		if prob >= 0.0:
			val += prob * pair[0] * pair[1]
			prob -= prob * pair[0]
		else:
			break
	return round(val)

def possibleEdgeMovesValue(player, board):
	possibilities = [(1.0, edgeTable[edgeIndex(player, board, topEdge)])]
	for sq in topEdge:
		if board[sq] == EMPTY:
			possibilities.append(possibleEdgeMove(player, board, sq))
	return combineEdgeMoves(possibilities, player)

def mapEdgeNPieces(fn, player, board, n, squares, index):
	if len(squares) < n:
		return
	elif not squares:
		fn(board, index)
	else:
		sq = squares[0]
		squaresRest = squares[1:]
		index3 = 3 * index
		mapEdgeNPieces(fn, player, board, n, squaresRest, index3)
		if n > 0 and board[sq] == EMPTY:
			board[sq] = player
			mapEdgeNPieces(fn, player, board, n - 1, squaresRest, index3 + 1)
			board[sq] = getOpponent(player)
			mapEdgeNPieces(fn, player, board, n - 1, squaresRest, index3 + 2)
			board[sq] = EMPTY

def initEdgeTable():
	board = getInitialBoard()
	for nPieces in xrange(10+1):
		mapEdgeNPieces(
			lambda board, index: setf(index, staticEdgeStability(BLACK, board)),
			BLACK,
			board,
			nPieces,
			topEdge,
			0 )
	for i in xrange(0):
		for nPieces in xrange(9, 0, -1): # for 9 downto 1
			mapEdgeNPieces(
				lambda board, index: setf(index, possibleEdgeMovesValue(BLACK, board)),
				BLACK,
				getInitialBoard(),
				nPieces,
				topEdge,
				0 )


def pieceStability(player, board, sq):
	stable = 0
	semiStable = 1
	unstable = 2

	stability = 0
	assert board != None and sq != None
	if board[sq] == EMPTY:
		return None
	
	if isCornerSquare(sq):
		stability = stable
	elif isXSquare(sq):
		stability = (unstable if board[cornerSquareForXSquare[sq]] == EMPTY else semiStable)
	else:
		opponent = getOpponent(player)
		end1 = end2 = -1
		i = topEdge.index(sq)
		while i < len(topEdge) - 1:
			end1 = board[topEdge[i]]
			if end1 != player:
				break
			i += 1
		i = topEdge.index(sq)
		while i > 0:
			end2 = board[topEdge[i]]
			if end2 != player:
				break
			i -= 1
		if (end1 == EMPTY and end2 == opponent) or (end2 == EMPTY and end1 == opponent):
			stability = unstable
		elif end1 == opponent and end2 == opponent and any(board[a] == EMPTY for a in topEdgeWithoutXs):
			stability = semiStable
		elif end1 == EMPTY and end2 == EMPTY:
			stability = semiStable
		else:
			stability = stable
	return stability

def staticEdgeStability(player, board):
	total = 0
	for i, sq in enumerate(topEdge):
		add = 0
		if board[sq] == EMPTY:
			add = 0
		else:
			add = staticEdgeTable[i][pieceStability(player, board, sq)]
			if board[sq] != player:
				add = -add
		total += add
	return total

initEdgeTable()
open('edgeTable.txt','w').write('edgeTable='+`edgeTable`.replace(" ",''))
f = open('weights.txt').read().replace('.0','')
open('weights.txt','w').write(f)