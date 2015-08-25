MOVE_SEC      = 0.01  #time to pause after move so that it can viewed

#which player starts first 'B' or 'W'
FIRST_PLAYER = 'B'

#below are the TCP/IP info for connecting servers and clients
TCP_PORT_1 = 12342
TCP_PORT_2 = 12452
BUF_SIZE   = 10240
TCP_IP     = '127.0.0.1'

TIME_BUF_SEC    =  1*60
TIME_LIMIT_SEC  = 25*60 + TIME_BUF_SEC  #total time given to each player to make moves
MEMORY_BUF_MB   = 2
MEMORY_LIMIT_MB = 80 + MEMORY_BUF_MB 

BRD_SIZE      = 8   #number of rows and columns on board
CELL_HW       = 70  #height and width of each cell on board
BRD_HW        = BRD_SIZE*CELL_HW #height and width of board
BRD_COLOR     = 'green' #color of game board
CURBOX_COLOR  = 'blue'  #color to highlight latest move
FLIP_COLOR    = 'red'   #color to highlight flipped pieces
CURBOX_BORDER = 5    #thickness of box to highlight latest move
FLIP_BORDER   = 3    #thickness of box to highlight flipped pieces
SLEEP_SEC     = 0.1  #interval to detect players' moves
FONT_SIZE     = 20   #size of font at top of game board
FONT_TYPE     = 'Helvetica' #type of font at top of game board

#below are directions for checking and creating moves
TOP_LEFT     = (-1,-1)
TOP          = (-1, 0)
TOP_RIGHT    = (-1, 1)
LEFT         = ( 0,-1)
RIGHT        = ( 0, 1)
BOTTOM_LEFT  = ( 1,-1)
BOTTOM       = ( 1, 0)
BOTTOM_RIGHT = ( 1, 1)
DIRECTIONS = (TOP_LEFT, TOP, TOP_RIGHT, LEFT, RIGHT, BOTTOM_LEFT, BOTTOM, BOTTOM_RIGHT)

