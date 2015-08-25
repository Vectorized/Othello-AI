import board, server, sys

if __name__ == '__main__':

	case = '0'

	if len(sys.argv) > 1:
		case = sys.argv[1]
		
	if case == '0' or case == 'test':
		board = board.Board()
		white = server.Server(1)
		black = server.Server(2)
		board.playGame(white, black)
	elif case == '1' or case == 'me':
		board = board.Board()
		white = board
		black = server.Server(2)
		board.playGame(white, black)
	elif case == '2' or case == 'he':
		board = board.Board()
		white = server.Server(1)
		black = board
		board.playGame(white, black)
