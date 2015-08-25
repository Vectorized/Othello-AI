import random, sys, time, math, itertools
from tables import *
from opening_book import *
from patterns_loader import *

"""
Throughout the code, you will see lots of magic hex numbers and bitwise operations.
The top reversi programs have enormous portions of their codebase devoted to 
speeding up the move generation and board evaluations. 
Evaluating even by a mere 6x faster can mean roughly 2 more levels of search near endgame.
Used correctly with a good search, all the factors combine synergetically to 
create a deep searching and smart program.

To understand more on the magic being used, here are some websites:
    https://chessprogramming.wikispaces.com/Flipping+Mirroring+and+Rotating
    https://chessprogramming.wikispaces.com/Kindergarten+Bitboards
    http://drpetric.blogspot.sg/2013/09/bit-gathering-via-multiplication.html

As this is Python, where ( + - * / << >> & ^ | ) operations on simple
numbers incurs lots of C pointer indirection overhead, 
we have used a new novel technique used called bitwise "vectorization",
where many numbers undergoing similar operations are packed into a 
single super giant number to do the operations on them in bulk.

Loops are unrolled whenever possible. 
Dictionary based lookups for small sets of values are preferred over functions.
"""

# Lookup for reversing 8 bits
revBits8 = [int(bin((256)|x)[-1:2:-1],2) for x in xrange(256)]

# Lookup for move number -> game stage
stageTable = [ 0, 
    0,  0,  0,  0,   0,  0,  0,  0,   0,  0,  0,  0, 
    1,  1,  1,  1,   2,  2,  2,  2,   3,  3,  3,  3, 
    4,  4,  4,  4,   5,  5,  5,  5,   6,  6,  6,  6, 
    7,  7,  7,  7,   8,  8,  8,  8,   9,  9,  9,  9, 
    10, 10, 10, 10,  11, 11, 11, 11,  12, 12, 12 ]

# Bounded memoize decorator
def memoize(f):
    class memodict(dict):
        def __missing__(self, key):
            c = self.__len__()
            if c > 50000:
                for k in self.keys()[:c/5]:
                    del self[k]
            ret = self[key] = f(key)
            return ret 
    return memodict().__getitem__

# chunks([1,2,3,4,5,6], 2) -> [[1,2],[3,4],[5,6]]
def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

# Mirror <64 bits player 1> - <64 bits spacer> - <64 bits player 2>
def horizontalMirrorDiscs(b):
    b =    ((b >> 1) & 0x555555555555555500000000000000005555555555555555) | ((b << 1) & 0xAAAAAAAAAAAAAAAA0000000000000000AAAAAAAAAAAAAAAA)
    b =    ((b >> 2) & 0x333333333333333300000000000000003333333333333333) | ((b << 2) & 0xCCCCCCCCCCCCCCCC0000000000000000CCCCCCCCCCCCCCCC)
    return ((b >> 4) & 0x0F0F0F0F0F0F0F0F00000000000000000F0F0F0F0F0F0F0F) | ((b << 4) & 0xF0F0F0F0F0F0F0F00000000000000000F0F0F0F0F0F0F0F0)

# Mirror <64 bits player 1> - <64 bits spacer> - <64 bits player 2>
def verticalMirrorDiscs(b):
    b =    ((b >>  8) & 0x00FF00FF00FF00FF000000000000000000FF00FF00FF00FF) | ((b <<  8) & 0xFF00FF00FF00FF000000000000000000FF00FF00FF00FF00)
    b =    ((b >> 16) & 0x0000FFFF0000FFFF00000000000000000000FFFF0000FFFF) | ((b << 16) & 0xFFFF0000FFFF00000000000000000000FFFF0000FFFF0000)
    return ((b >> 32) & 0x00000000FFFFFFFF000000000000000000000000FFFFFFFF) | ((b << 32) & 0xFFFFFFFF000000000000000000000000FFFFFFFF00000000)

# Transpose <64 bits player 1> - <64 bits spacer> - <64 bits player 2>
def diagMirrorDiscs(b):
    t = (b ^ (b >> 7))  & 0x00aa00aa00aa00aa000000000000000000aa00aa00aa00aa
    b = b ^ t ^ (t << 7)
    t = (b ^ (b >> 14)) & 0x0000cccc0000cccc00000000000000000000cccc0000cccc
    b = b ^ t ^ (t << 14)
    t = (b ^ (b >> 28)) & 0x00000000f0f0f0f0000000000000000000000000f0f0f0f0
    return (b ^ t ^ (t << 28)) & 0xFFFFFFFFFFFFFFFF0000000000000000FFFFFFFFFFFFFFFF

# Transpose <64 bits player 1> - <64 bits spacer> - <64 bits player 2> on anti-diagonal
def antiDiagMirrorDiscs(b):
    t  = b ^ (b << 36)
    b ^= 0xf0f0f0f00f0f0f0f0000000000000000f0f0f0f00f0f0f0f & (t ^ (b >> 36))
    t  = 0xcccc0000cccc00000000000000000000cccc0000cccc0000 & (b ^ (b << 18))
    b ^= t ^ (t >> 18)
    t  = 0xaa00aa00aa00aa000000000000000000aa00aa00aa00aa00 & (b ^ (b <<  9))
    return (b ^ t ^ (t >>  9)) & 0xFFFFFFFFFFFFFFFF0000000000000000FFFFFFFFFFFFFFFF

def horizontalMirrorDiscsSingle(b):
    b =    ((b >> 1) & 0x5555555555555555) | ((b << 1) & 0xAAAAAAAAAAAAAAAA)
    b =    ((b >> 2) & 0x3333333333333333) | ((b << 2) & 0xCCCCCCCCCCCCCCCC)
    return ((b >> 4) & 0x0F0F0F0F0F0F0F0F) | ((b << 4) & 0xF0F0F0F0F0F0F0F0)

def verticalMirrorDiscsSingle(b):
    b =    ((b >>  8) & 0x00FF00FF00FF00FF) | ((b <<  8) & 0xFF00FF00FF00FF00)
    b =    ((b >> 16) & 0x0000FFFF0000FFFF) | ((b << 16) & 0xFFFF0000FFFF0000)
    return ((b >> 32) & 0x00000000FFFFFFFF) | ((b << 32) & 0xFFFFFFFF00000000)

def diagMirrorDiscsSingle(b):
    t = (b ^ (b >> 7)) & 0x00aa00aa00aa00aa
    b = b ^ t ^ (t << 7)
    t = (b ^ (b >> 14)) & 0x0000cccc0000cccc
    b = b ^ t ^ (t << 14)
    t = (b ^ (b >> 28)) & 0x00000000f0f0f0f0
    return b ^ t ^ (t << 28)

def antiDiagMirrorDiscsSingle(b):
    t  = b ^ (b << 36)
    b ^= 0xf0f0f0f00f0f0f0f & (t ^ (b >> 36))
    t  = 0xcccc0000cccc0000 & (b ^ (b << 18))
    b ^= t ^ (t >> 18)
    t  = 0xaa00aa00aa00aa00 & (b ^ (b <<  9))
    return b ^ t ^ (t >>  9)

# Get the next board with the move and reversed discs
def getPut(player, opponent, move, rev):
    return player ^ (move | rev), opponent ^ rev

def getNumEmptiesLeft(player, opponent):
    return (64 - bin(player | opponent).count("1")) 

# Returns [(move_0, rev_0), ...]
def getMoves(player, opponent):
    blank = ~ (player | opponent)
    # Get mobility Left
    w = opponent & 0x7e7e7e7e7e7e7e7e
    t = w & (player >> 1)
    t |= w & (t >> 1); v = w & (w >> 1); t |= v & (t >> 2);  t |= v & (t >> 2)
    rLeft = blank & (t >> 1)
    # Get mobility Right
    t = w & (player << 1)
    t |= w & (t << 1); v = w & (w << 1); t |= v & (t << 2);  t |= v & (t << 2)
    rRight = blank & (t << 1)
    # Get mobility Top
    w = opponent & 0x00ffffffffffff00
    t = w & (player >> 8)
    t |= w & (t >> 8); v = w & (w >> 8); t |= v & (t >> 16); t |= v & (t >> 16)
    rTop = blank & (t >> 8)
    # Get mobility Bottom
    t = w & (player << 8)
    t |= w & (t << 8); v = w & (w << 8); t |= v & (t << 16); t |= v & (t << 16)
    rBottom = blank & (t << 8)
    # Get mobility Left Top
    w = opponent & 0x007e7e7e7e7e7e00
    t = w & (player >> 9);
    t |= w & (t >> 9); v = w & (w >> 9); t |= v & (t >> 18); t |= v & (t >> 18)
    rLeftTop = blank & (t >> 9)
    # Get mobility Left Bottom
    t = w & (player << 7)
    t |= w & (t << 7); v = w & (w << 7); t |= v & (t << 14); t |= v & (t << 14)
    rLeftBottom = blank & (t << 7)
    # Get mobility Right Top
    t = w & (player >> 7)
    t |= w & (t >> 7); v = w & (w >> 7); t |= v & (t >> 14); t |= v & (t >> 14)
    rRightTop = blank & (t >> 7)
    # Get mobility Right Bottom
    t = w & (player << 9)
    t |= w & (t << 9); v = w & (w << 9); t |= v & (t << 18); t |= v & (t << 18)
    rRightBottom = blank & (t << 9)
    r = rLeft | rRight | rTop | rBottom | rLeftTop | rLeftBottom | rRightTop | rRightBottom
    # Extract moves and reversed tiles
    moves = []
    while r:
        m = r & -r
        rev = 0
        # Left
        if rLeft & m:
            mask = (m << 1) & 0xfefefefefefefefe
            if mask:
                _rev = 0
                while mask & opponent:
                    _rev |= mask
                    mask = (mask << 1) & 0xfefefefefefefefe
                if mask & player:
                    rev |= _rev
        # Right
        if rRight & m:
            mask = (m >> 1) & 0x7f7f7f7f7f7f7f7f
            if mask:
                _rev = 0
                while mask & opponent:
                    _rev |= mask
                    mask = (mask >> 1) & 0x7f7f7f7f7f7f7f7f
                if mask & player:
                    rev |= _rev
        # Top
        if rTop & m:
            mask = (m << 8) & 0xffffffffffffff00
            if mask:
                _rev = 0
                while mask & opponent:
                    _rev |= mask
                    mask = (mask << 8) & 0xffffffffffffff00
                if mask & player:
                    rev |= _rev
        # Bottom
        if rBottom & m:
            mask = (m >> 8) & 0x00ffffffffffffff
            if mask:
                _rev = 0
                while mask & opponent:
                    _rev |= mask
                    mask = (mask >> 8) & 0x00ffffffffffffff
                if mask & player:
                    rev |= _rev
        # Left Top
        if rLeftTop & m:
            mask = (m << 9) & 0xfefefefefefefe00
            if mask:
                _rev = 0
                while mask & opponent:
                    _rev |= mask
                    mask = (mask << 9) & 0xfefefefefefefe00
                if mask & player:
                    rev |= _rev
        # Left Bottom
        if rLeftBottom & m:
            mask = (m >> 7) & 0x00fefefefefefefe
            if mask:
                _rev = 0
                while mask & opponent:
                    _rev |= mask
                    mask = (mask >> 7) & 0x00fefefefefefefe
                if mask & player:
                    rev |= _rev
        # Right Top
        if rRightTop & m:
            mask = (m << 7) & 0x7f7f7f7f7f7f7f00
            if mask:
                _rev = 0
                while mask & opponent:
                    _rev |= mask
                    mask = (mask << 7) & 0x7f7f7f7f7f7f7f00
                if mask & player:
                    rev |= _rev
        # Right Bottom
        if rRightBottom & m:
            mask = (m >> 9) & 0x007f7f7f7f7f7f7f
            if mask:
                _rev = 0
                while mask & opponent:
                    _rev |= mask
                    mask = (mask >> 9) & 0x007f7f7f7f7f7f7f
                if mask & player:
                    rev |= _rev

        moves.append((m, rev)) # Append move and reversed tiles
        r &= r - 1 # Remove smallest bit

    return moves

# Final board value for search when hit the end
def finalBoardValue(player, opponent):
    playerCount = bin(player).count("1")
    opponentCount = bin(opponent).count("1")
    # These "infinities" must be incrementable integers/longs
    # for negascout's "b = alpha + 1" to work.
    if playerCount > opponentCount: # Win
        return 1<<50 
    return -(1<<50)

# Actual move -> unique move
def getSymmetricMoveSingle(discs, symmetryIndex):
    if symmetryIndex == 0:
        return discs
    if symmetryIndex == 1: 
        return horizontalMirrorDiscsSingle(discs)
    if symmetryIndex == 2: 
        return verticalMirrorDiscsSingle(discs)
    if symmetryIndex == 3: 
        return horizontalMirrorDiscsSingle(verticalMirrorDiscsSingle(discs))
    if symmetryIndex == 4:
        return diagMirrorDiscsSingle(discs)
    if symmetryIndex == 5:
        return antiDiagMirrorDiscsSingle(discs)
    if symmetryIndex == 6:
        return verticalMirrorDiscsSingle(antiDiagMirrorDiscsSingle(discs))
    if symmetryIndex == 7:
        return verticalMirrorDiscsSingle(diagMirrorDiscsSingle(discs))
    return discs

# Unique move -> actual move
def getSymmetricMoveSingleInverse(discs, symmetryIndex):
    if symmetryIndex == 0:
        return discs
    if symmetryIndex == 1: 
        return horizontalMirrorDiscsSingle(discs)
    if symmetryIndex == 2: 
        return verticalMirrorDiscsSingle(discs)
    if symmetryIndex == 3: 
        return verticalMirrorDiscsSingle(horizontalMirrorDiscsSingle(discs))
    if symmetryIndex == 4:
        return diagMirrorDiscsSingle(discs)
    if symmetryIndex == 5:
        return antiDiagMirrorDiscsSingle(discs)
    if symmetryIndex == 6:
        return antiDiagMirrorDiscsSingle(verticalMirrorDiscsSingle(discs))
    if symmetryIndex == 7:
        return diagMirrorDiscsSingle(verticalMirrorDiscsSingle(discs))
    return discs

# Actual board -> unique board, symmetry index
# combined is: (player << 128) | opponent
def getUniqueBoard(combined):
    unique = combined
    symmetryIndex = 0
    # mirror hori
    symmetry1 = horizontalMirrorDiscs(combined)
    # mirror vert
    symmetry2 = verticalMirrorDiscs(combined)
    # rotate 180 degrees
    symmetry3 = horizontalMirrorDiscs(symmetry2)
    # flip diagonal
    symmetry4 = diagMirrorDiscs(combined)
    # flip anti-diagonal
    symmetry5 = antiDiagMirrorDiscs(combined)
    # 90 degrees CW
    symmetry6 = verticalMirrorDiscs(symmetry5)
    # 90 degrees Anti-CW
    symmetry7 = verticalMirrorDiscs(symmetry4)
    # Get min to be unique
    if symmetry1 < unique: unique = symmetry1; symmetryIndex = 1
    if symmetry2 < unique: unique = symmetry2; symmetryIndex = 2
    if symmetry3 < unique: unique = symmetry3; symmetryIndex = 3
    if symmetry4 < unique: unique = symmetry4; symmetryIndex = 4
    if symmetry5 < unique: unique = symmetry5; symmetryIndex = 5
    if symmetry6 < unique: unique = symmetry6; symmetryIndex = 6
    if symmetry7 < unique: unique = symmetry7; symmetryIndex = 7
    return unique, symmetryIndex

# The pattern based evaluation function for search leafs
def evalBoard(player, opponent):
    combined = player | opponent
    if combined == 0xFFFFFFFFFFFFFFFF: # If game over... return final board value.
        return finalBoardValue(player, opponent)
    s = stageTable[bin(combined).count("1") - 4]

    # We combine player and opponent for "vectorized" bitwise operations
    combinedPO = (player << 128) | opponent

    # Magic kindergarten board bit collection for each feature
    # Diagonals:
    diagA4D1MaskMul = (combinedPO & 0x102040800000000000000000000000001020408000000000L) * 16843009
    diagA5D8MaskMul = (combinedPO & 0x8040201000000000000000000000000080402010L) * 72340172821233664
    diagH4E1MaskMul = (combinedPO & 0x80402010000000000000000000000000804020100000000L) * 2149582850
    diagH5E8MaskMul = (combinedPO & 0x102040800000000000000000000000001020408L) * 2130440
    diagA5E1MaskMul = (combinedPO & 0x81020408000000000000000000000000810204080000000L) * 4311810305
    diagA4E8MaskMul = (combinedPO & 0x804020100800000000000000000000008040201008L) * 72340172838010880
    diagH5D1MaskMul = (combinedPO >> 21 & 0x804020100800000000000000000000008040201008L) * 2201172838402
    diagH4D8MaskMul = (combinedPO & 0x10204081000000000000000000000000102040810L) * 36600682651844608
    diagA6F1MaskMul = (combinedPO & 0x40810204080000000000000000000000408102040800000L) * 1103823438081
    diagA3F8MaskMul = (combinedPO & 0x80402010080400000000000000000000804020100804L) * 72340172838076416
    diagH3C8MaskMul = (combinedPO & 0x1020408102000000000000000000000010204081020L) * 9150170671349760
    diagH6C1MaskMul = (combinedPO >> 16 & 0x20100804020100000000000000000000201008040201L) * 9016003946094600
    diagA7G1MaskMul = (combinedPO & 0x20408102040800000000000000000000204081020408000L) * 282578800148737
    diagA2G8MaskMul = (combinedPO & 0x8040201008040200000000000000000080402010080402L) * 72340172838076672
    diagH2B8MaskMul = (combinedPO & 0x102040810204000000000000000000001020408102040L) * 2287542667870208
    diagH7B1MaskMul = (combinedPO >> 6 & 0x10080402010080400000000000000000100804020100804L) * 1154048505100108801
    diag8MaskMulA = (combinedPO & 0x804020100804020100000000000000008040201008040201L) * 72340172838076673
    diag8MaskMulB = (combinedPO & 0x10204081020408000000000000000000102040810204080L) * 72340172838076673
    # Columns
    colAMaskMul = (combinedPO & 0x808080808080808000000000000000008080808080808080L) * 567382630219905
    colBMaskMul = (combinedPO & 0x404040404040404000000000000000004040404040404040L) * 1134765260439810
    colCMaskMul = (combinedPO & 0x202020202020202000000000000000002020202020202020L) * 2269530520879620
    colDMaskMul = (combinedPO & 0x101010101010101000000000000000001010101010101010L) * 4539061041759240
    colEMaskMul = (combinedPO & 0x80808080808080800000000000000000808080808080808L) * 9078122083518480
    colFMaskMul = (combinedPO & 0x40404040404040400000000000000000404040404040404L) * 18156244167036960
    colGMaskMul = (combinedPO & 0x20202020202020200000000000000000202020202020202L) * 36312488334073920
    colHMaskMul = (combinedPO & 0x10101010101010100000000000000000101010101010101L) * 72624976668147840
    # 4x2 Corners.. some corners need 2x bit gathers due to inconvenient orientation
    cornA1B4MaskMulA = (combinedPO & 0x808080800000000000000000000000008080808000000000L) * 270549121
    cornA1B4MaskMulB = (combinedPO & 0x404040400000000000000000000000004040404000000000L) * 270549121
    cornA8B5MaskMulA = (combinedPO & 0x8080808000000000000000000000000080808080L) * 270549121
    cornA8B5MaskMulB = (combinedPO & 0x4040404000000000000000000000000040404040L) * 270549121
    cornA8D7MaskMul = (combinedPO & 0xf0f00000000000000000000000000000f0f0L) * 4097
    cornH8E7MaskMul = (combinedPO & 0xf0f00000000000000000000000000000f0fL) * 17
    cornH8G5MaskMulA = (combinedPO & 0x101010100000000000000000000000001010101L) * 270549121
    cornH8G5MaskMulB = (combinedPO & 0x202020200000000000000000000000002020202L) * 270549121
    cornH1G4MaskMulA = (combinedPO & 0x20202020000000000000000000000000202020200000000L) * 270549121
    cornH1G4MaskMulB = (combinedPO & 0x10101010000000000000000000000000101010100000000L) * 270549121
    cornA1D2MaskMul = (combinedPO & 0xf0f00000000000000000000000000000f0f0000000000000L) * 17
    cornH1E2MaskMul = (combinedPO & 0xf0f00000000000000000000000000000f0f000000000000L) * 4097

    # Lookup values for each feature and return the sum
    return (
        # Length 4 diagonals
        diag4[s][base2To3[diagA4D1MaskMul >> 188 & 0xF] - base2To3[diagA4D1MaskMul >> 60 & 0xF] ] +
        diag4[s][base2To3[diagA5D8MaskMul >> 188 & 15] - base2To3[diagA5D8MaskMul >> 60 & 15] ] +
        diag4[s][base2To3[diagH4E1MaskMul >> 188 & 0Xf] - base2To3[diagH4E1MaskMul >> 60 & 0Xf] ] +
        diag4[s][base2To3[diagH5E8MaskMul >> 152 & 0xF] - base2To3[diagH5E8MaskMul >> 24 & 0xF] ] +
        # Length 5 diagonals
        diag5[s][base2To3[diagA5E1MaskMul >> 187 & 0x1F] - base2To3[diagA5E1MaskMul >> 59 & 0x1F] ] +
        diag5[s][base2To3[diagA4E8MaskMul >> 187 & 31] - base2To3[diagA4E8MaskMul >> 59 & 31] ] +
        diag5[s][base2To3[diagH5D1MaskMul >> 168 & 0x1F] - base2To3[diagH5D1MaskMul  >> 40 & 0x1F] ] +
        diag5[s][base2To3[diagH4D8MaskMul >> 187 & 31] - base2To3[diagH4D8MaskMul >> 59 & 31] ] +
        # Length 6 diagonals
        diag6[s][base2To3[diagA6F1MaskMul >> 186 & 0x3F] - base2To3[diagA6F1MaskMul >> 58 & 0x3F] ] +
        diag6[s][base2To3[diagA3F8MaskMul >> 186 & 63] - base2To3[diagA3F8MaskMul >> 58 & 63] ] +
        diag6[s][base2To3[diagH3C8MaskMul >> 186 & 63] - base2To3[diagH3C8MaskMul >> 58 & 63] ] +
        diag6[s][base2To3[diagH6C1MaskMul >> 176 & 0x3F] - base2To3[diagH6C1MaskMul  >> 48 & 0x3F] ] +
        # Length 7 diagonals
        diag7[s][base2To3[diagA7G1MaskMul >> 185 & 127] - base2To3[diagA7G1MaskMul >> 57 & 127] ] +
        diag7[s][base2To3[diagA2G8MaskMul >> 185 & 127] - base2To3[diagA2G8MaskMul >> 57 & 127] ] +
        diag7[s][base2To3[diagH2B8MaskMul >> 185 & 127] - base2To3[diagH2B8MaskMul >> 57 & 127] ] +
        diag7[s][base2To3[diagH7B1MaskMul >> 184 & 127] - base2To3[diagH7B1MaskMul  >> 56 & 127] ] +
        # Length 8 diagonals
        diag8[s][base2To3[diag8MaskMulA >> 184 & 0xff] - base2To3[diag8MaskMulA >> 56 & 0xff] ] +
        diag8[s][base2To3[diag8MaskMulB >> 184 & 0xFF] - base2To3[diag8MaskMulB >> 56 & 0xFF] ] +
        # Rows
        lc1[s][base2To3[(player >> 56) & 0xFF] - base2To3[(opponent >> 56) & 0xFF] ] +
        lc2[s][base2To3[(player >> 48) & 0xFF] - base2To3[(opponent >> 48) & 0xFF] ] +
        lc3[s][base2To3[(player >> 40) & 0xFF] - base2To3[(opponent >> 40) & 0xFF] ] +
        lc4[s][base2To3[(player >> 32) & 0xFF] - base2To3[(opponent >> 32) & 0xFF] ] +
        lc4[s][base2To3[(player >> 24) & 0xFF] - base2To3[(opponent >> 24) & 0xFF] ] +
        lc3[s][base2To3[(player >> 16) & 0xFF] - base2To3[(opponent >> 16) & 0xFF] ] +
        lc2[s][base2To3[(player >> 8)  & 0xFF] - base2To3[(opponent >> 8)  & 0xFF] ] +
        lc1[s][base2To3[player & 0xFF] - base2To3[opponent & 0xFF] ] +
        # Columns
        lc1[s][base2To3[colAMaskMul >> 184 & 0xff] - base2To3[colAMaskMul >> 56 & 0xff] ] +
        lc2[s][base2To3[colBMaskMul >> 184 & 0xff] - base2To3[colBMaskMul >> 56 & 0xff] ] +
        lc3[s][base2To3[colCMaskMul >> 184 & 0xff] - base2To3[colCMaskMul >> 56 & 0xff] ] +
        lc4[s][base2To3[colDMaskMul >> 184 & 0xff] - base2To3[colDMaskMul >> 56 & 0xff] ] +
        lc4[s][base2To3[colEMaskMul >> 184 & 0xff] - base2To3[colEMaskMul >> 56 & 0xff] ] +
        lc3[s][base2To3[colFMaskMul >> 184 & 0xff] - base2To3[colFMaskMul >> 56 & 0xff] ] +
        lc2[s][base2To3[colGMaskMul >> 184 & 0xff] - base2To3[colGMaskMul >> 56 & 0xff] ] +
        lc1[s][base2To3[colHMaskMul >> 184 & 0xff] - base2To3[colHMaskMul >> 56 & 0xff] ] +
        # 4x2 corners
        corn[s][base2To3[((cornA1B4MaskMulA >> 184 & 240) |(cornA1B4MaskMulB >> 187 & 15) )] - base2To3[((cornA1B4MaskMulA >> 56 & 240) |(cornA1B4MaskMulB >> 59 & 15) )] ] +
        corn[s][base2To3[(revBits8[cornA8B5MaskMulA >> 156 & 15] | revBits8[cornA8B5MaskMulB >> 151 & 240] )] - base2To3[(revBits8[cornA8B5MaskMulA >> 28 & 15] | revBits8[cornA8B5MaskMulB >> 23 & 240]  )] ] +
        corn[s][base2To3[cornA8D7MaskMul >> 140 & 255] - base2To3[cornA8D7MaskMul >> 12 & 255] ] +
        corn[s][base2To3[revBits8[cornH8E7MaskMul >> 132 & 255]] - base2To3[revBits8[cornH8E7MaskMul >> 4 & 255]] ] +
        corn[s][base2To3[(revBits8[cornH8G5MaskMulA >> 149 & 15] | revBits8[cornH8G5MaskMulB >> 146 & 240] )] - base2To3[(revBits8[cornH8G5MaskMulA >> 21 & 15] | revBits8[cornH8G5MaskMulB >> 18 & 240] )] ] +
        corn[s][base2To3[((cornH1G4MaskMulA >> 182 & 15) | (cornH1G4MaskMulB >> 177 & 240) )] - base2To3[((cornH1G4MaskMulA >> 54 & 15) |(cornH1G4MaskMulB >> 49 & 240) )] ] +
        corn[s][base2To3[cornA1D2MaskMul >> 184 & 255] - base2To3[cornA1D2MaskMul >> 56 & 255] ] +
        corn[s][base2To3[revBits8[cornH1E2MaskMul >> 184 & 255]] - base2To3[revBits8[cornH1E2MaskMul >> 56 & 255]] ] +
        # Parity
        parity[s][(60-s)&1]
    )

# Convert from the game engine board -> bitboard
def makeBitBoard(board, playerColor):
    b = [a for b in board for a in b]
    opponentColor = 'W' if playerColor=='B' else 'B'
    return reduce(lambda m,n:m*2+(n==playerColor),b,0), reduce(lambda m,n:m*2+(n==opponentColor),b,0)

# Print the bitboard
def printBitBoard(player, opponent=None, playerColor=None, printCoors=True):
    ss = []
    opponentColor = 'W' if playerColor=='B' else 'B'
    if printCoors:
        ss.append('  A B C D E F G H\n')
    for i in xrange(8):
        if printCoors:
            ss.append(str(i+1)+' ') 
        for j in xrange(8):
            if opponent != None:
                if player&(2**((7-i)*8+(7-j))): ss.append(playerColor+' ')
                elif opponent&(2**((7-i)*8+(7-j))): ss.append(opponentColor+' ')
                else: ss.append('_ ')
            else:
                if player&(2**((7-i)*8+(7-j))): ss.append('X ')
                else: ss.append('_ ')
        ss.append('\n')
    print "".join(ss)

# Get start board
def getStartBoard():
    return 34628173824, 68853694464

# Simulate a random game of and return the board
# Used for debugging and tuning purposes
def getRandomBoard(numMoves = 15):
    p, o = getStartBoard()
    for x in xrange(numMoves):
        moves = getMoves(p, o)
        if moves:
            m, r = random.choice(moves)
            o, p = getPut(p, o, m, r)
        else:
            o, p = p, o
    return p, o

# Simulate a random game, and return the consecutive boards after that
# Used for debugging and tuning purposes
def getRandomBoards(start = 15, numMoves = 15):
    p, o = getRandomBoard(start)
    boards = [(p, o)]
    for x in xrange(numMoves):
        moves = getMoves(p, o)
        if moves:
            m, r = random.choice(moves)
            o, p = getPut(p, o, m, r)
        else:
            o, p = p, o
        boards.append((p, o))
    return boards

# 0b101001 -> [0b1, 0b1000, 0b100000]
def bits(x):
    while x:
        yield x&-x
        x=x&(x-1)

# Is it game over already?
def isGameOver(player, opponent):
    return bin(player | opponent).count("1") == 64

# Just some values for debug and tuning purposes
x = list(chunks([["G","B","W"][i] for i in 
      [ 2, 0, 0, 2, 2, 2, 2, 1,
        0, 2, 2, 2, 2, 2, 2, 1,
        2, 2, 1, 1, 2, 2, 2, 1,
        2, 2, 1, 2, 2, 2, 1, 1,
        2, 2, 2, 2, 2, 2, 1, 1,
        0, 0, 0, 2, 2, 2, 2, 1,
        0, 0, 0, 0, 2, 0, 1, 1,
        0, 0, 0, 0, 0, 0, 0, 2]], 8))
testPlayer, testOpponent = makeBitBoard(list(x), 'B')

# Precalculated bitmasks for "vectorized" bitwise operations in our move ordering evaluation function
mobilityMasks0          = [0, 0x7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e]
mobilityMasks1          = [0, 0x00ffffffffffff0000ffffffffffff00]
mobilityMasks2          = [0, 0x007e7e7e7e7e7e00007e7e7e7e7e7e00]
potentialMoblityMasksL1 = [0, 0xfefefefefefefefefefefefefefefefe]
potentialMoblityMasksR1 = [0, 0x7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f]
potentialMoblityMasksL8 = [0, 0xffffffffffffff00ffffffffffffff00]
potentialMoblityMasksR8 = [0, 0x00ffffffffffffff00ffffffffffffff]
potentialMoblityMasksL9 = [0, 0xfefefefefefefe00fefefefefefefe00]
potentialMoblityMasksR7 = [0, 0x00fefefefefefefe00fefefefefefefe]
potentialMoblityMasksL7 = [0, 0x7f7f7f7f7f7f7f007f7f7f7f7f7f7f00]
potentialMoblityMasksR9 = [0, 0x007f7f7f7f7f7f7f007f7f7f7f7f7f7f]
popCountFrames          = [0, 1<<128]
for x in xrange(60):
    mobilityMasks0.append((mobilityMasks0[-1] << 129) | mobilityMasks0[1])
    mobilityMasks1.append((mobilityMasks1[-1] << 129) | mobilityMasks1[1])
    mobilityMasks2.append((mobilityMasks2[-1] << 129) | mobilityMasks2[1])
    potentialMoblityMasksL1.append((potentialMoblityMasksL1[-1] << 129) | potentialMoblityMasksL1[1])
    potentialMoblityMasksR1.append((potentialMoblityMasksR1[-1] << 129) | potentialMoblityMasksR1[1])
    potentialMoblityMasksL8.append((potentialMoblityMasksL8[-1] << 129) | potentialMoblityMasksL8[1])
    potentialMoblityMasksR8.append((potentialMoblityMasksR8[-1] << 129) | potentialMoblityMasksR8[1])
    potentialMoblityMasksL9.append((potentialMoblityMasksL9[-1] << 129) | potentialMoblityMasksL9[1])
    potentialMoblityMasksR7.append((potentialMoblityMasksR7[-1] << 129) | potentialMoblityMasksR7[1])
    potentialMoblityMasksL7.append((potentialMoblityMasksL7[-1] << 129) | potentialMoblityMasksL7[1])
    potentialMoblityMasksR9.append((potentialMoblityMasksR9[-1] << 129) | potentialMoblityMasksR9[1])
    popCountFrames.append((popCountFrames[-1] << 129) | popCountFrames[1])


# Returns an estimate on how stable is an edge using precalculated values.
@memoize
def getEdgeStability(combinedPO):
    player = combinedPO >> 64
    opponent = combinedPO & 0xFFFFFFFFFFFFFFFF

    # Edge stability using magic kindergarten bit gathering methods
    playerB2L = (player & 0x40000000000000) >> 45
    opponentB2L = (opponent & 0x40000000000000) >> 45

    playerG7R = (player & 0x200) >> 9
    opponentG7R = (opponent & 0x200) >> 9

    playerG2 = (player & 0x2000000000000)
    opponentG2 = (opponent & 0x2000000000000) 
    playerG2L = playerG2 >> 40
    playerG2R = playerG2 >> 49
    opponentG2L = opponentG2 >> 40
    opponentG2R = opponentG2 >> 49

    playerB7 = (player & 0x4000)
    opponentB7 = (opponent & 0x4000) 
    playerB7L = playerB7 >> 5
    playerB7R = playerB7 >> 14
    opponentB7L = opponentB7 >> 5
    opponentB7R = opponentB7 >> 14

    # left
    playerLeft = playerB2L | ((((player & 0x8080808080808080L) * 567382630219905) >> 55) & 510) | playerB7R
    opponentLeft = opponentB2L | ((((opponent & 0x8080808080808080L) * 567382630219905) >> 55) & 510) | opponentB7R
    leftIndex = base2To3[playerLeft] + 2 * base2To3[opponentLeft]

    #right
    playerRight = playerG2L | ((((player & 0x101010101010101) * 72624976668147840) >> 55) & 510) | playerG7R
    opponentRight = opponentG2L | ((((opponent & 0x101010101010101) * 72624976668147840) >> 55) & 510) | opponentG7R
    rightIndex = base2To3[playerRight] + 2 * base2To3[opponentRight]

    # top
    playerTop = playerB2L | ((player & 0xff00000000000000L) >> 55) | playerG2R
    opponentTop = opponentB2L | ((opponent & 0xff00000000000000L) >> 55) | opponentG2R
    topIndex = base2To3[playerTop] + 2 * base2To3[opponentTop]

    # bottom
    playerBottom = playerB7L | ((player & 0xff) << 1) | playerG7R
    opponentBottom = opponentB7L | ((opponent & 0xff) << 1) | opponentG7R
    bottomIndex = base2To3[playerBottom] + 2 * base2To3[opponentBottom]

    return edgeTable[topIndex] + edgeTable[bottomIndex] + edgeTable[leftIndex] + edgeTable[rightIndex]

# Evaluate a whole list of boards for move ordering.
# The values are already sufficiently accurate for serious play.
def evalBoardsMoveOrderingVectorized(boards):
    vectorizedOP = 0
    vectorizedPO = 0
    vectorizedBlank = 0
    moveNumber = bin(boards[0][0] | boards[0][1]).count("1") - 3

    # Edge's weight
    cEdg = 312000 + 6240 * moveNumber 
    # Mobility differential's weight
    cCur = 50000 + 2000 * moveNumber if moveNumber < 25 else 75000 + 1000 * moveNumber
    # Potential mobility differential's weight
    cPot = 20000

    numBoards = len(boards)
    values = [0] * numBoards

    i = 0
    for player, opponent in boards:
        vectorizedBlank = (vectorizedBlank << 129) | (~(player | opponent) & 0xFFFFFFFFFFFFFFFF)
        combinedPO = ((player << 64) | opponent)
        vectorizedOP = (vectorizedOP << 129) | ((opponent << 64) | player)
        vectorizedPO = (vectorizedPO << 129) | combinedPO
        # Add edge stability
        values[i] = (cEdg * getEdgeStability(combinedPO & 0xffc381818181c3ffffc381818181c3ff)) / 32000 
        i += 1

    vectorizedBlank *= 0x10000000000000001
    # Get mobility Left
    w = vectorizedOP & mobilityMasks0[numBoards]
    sR1 = vectorizedPO >> 1
    t = w & sR1
    t |= w & (t >> 1); v = w & (w >> 1); t |= v & (t >> 2); t |= v & (t >> 2)
    r = t >> 1
    # Get mobility Right
    sL1 = vectorizedPO << 1
    t = w & sL1
    t |= w & (t << 1); v = w & (w << 1); t |= v & (t << 2); t |= v & (t << 2)
    r |= t << 1
    # Get mobility Top
    w = vectorizedOP & mobilityMasks1[numBoards]
    sR8 = vectorizedPO >> 8
    t = w & sR8
    t |= w & (t >> 8); v = w & (w >> 8); t |= v & (t >> 16); t |= v & (t >> 16)
    r |= t >> 8
    # Get mobility Bottom
    sL8 = vectorizedPO << 8
    t = w & sL8
    t |= w & (t << 8); v = w & (w << 8); t |= v & (t << 16); t |= v & (t << 16)
    r |= t << 8
    # Get mobility Left Top
    w = vectorizedOP & mobilityMasks2[numBoards]
    sR9 = vectorizedPO >> 9
    t = w & sR9
    t |= w & (t >> 9); v = w & (w >> 9); t |= v & (t >> 18); t |= v & (t >> 18)
    r |= t >> 9
    # Get mobility Left Bottom
    sL7 = vectorizedPO << 7
    t = w & sL7
    t |= w & (t << 7); v = w & (w << 7); t |= v & (t << 14); t |= v & (t << 14)
    r |= t << 7
    # Get mobility Right Top
    sR7 = vectorizedPO >> 7
    t = w & sR7
    t |= w & (t >> 7); v = w & (w >> 7); t |= v & (t >> 14); t |= v & (t >> 14)
    r |= t >> 7
    # Get mobility Right Bottom
    sL9 = vectorizedPO << 9
    t = w & sL9
    t |= w & (t << 9); v = w & (w << 9); t |= v & (t << 18); t |= v & (t << 18)
    r |= t << 9

    # Get potential mobility
    vectorizedPotentialMobility = (
        (sL1 & potentialMoblityMasksL1[numBoards]) |
        (sR1 & potentialMoblityMasksR1[numBoards]) |
        (sL8 & potentialMoblityMasksL8[numBoards]) |
        (sR8 & potentialMoblityMasksR8[numBoards]) |
        (sL9 & potentialMoblityMasksL9[numBoards]) |
        (sR7 & potentialMoblityMasksR7[numBoards]) |
        (sL7 & potentialMoblityMasksL7[numBoards]) |
        (sR9 & potentialMoblityMasksR9[numBoards]) )
    
    frame = popCountFrames[numBoards]
    binR = bin((r & vectorizedBlank) | frame)
    binPotentialMobility = bin((vectorizedPotentialMobility & vectorizedBlank) | frame)
    leftStartIndex = 3
    midIndex = 67
    rightEndIndex = 131

    i = 0
    # Count the bits to know the mobilities and potential mobilities
    for player, opponent in boards: 
        pMobCur = binR.count("1", leftStartIndex, midIndex)
        pMobPot = binPotentialMobility.count("1", midIndex, rightEndIndex)
        oMobCur = binR.count("1", midIndex, rightEndIndex)
        oMobPot = binPotentialMobility.count("1", leftStartIndex, midIndex)
        leftStartIndex += 129
        midIndex += 129
        rightEndIndex += 129

        values[i] += ( 
        # Mobility differential
        (cCur * (pMobCur - oMobCur)) / (pMobCur + oMobCur + 2) + 
        # Potential mobility differential
        (cPot * (pMobPot - oMobPot)) / (pMobPot + oMobPot + 2) )

        i += 1

    return values

# A Negascout, which is similar to Principle Variation Search (PVS) in this case
# Uses move ordering and tranposition table
# Note that the depth here refers to how much deeper to search: Max at root, 0 at leafs
def reversiABNegaScout(player, opponent, depth, depthCounters = None, 
    alpha = -(1<<48), beta = 1<<48, isRoot = True, tranpositionTable = None):
    # Increment how many nodes at the current depth.
    if depthCounters:
        depthCounters[depth] += 1
    # Leaf
    if depth == 0:
        return evalBoard(player, opponent)
    else: # Not Leaf
        if isRoot:
            tranpositionTable = {}
        else:
            try: # Try to see if the transposition table has a previously searched value
                lookup = tranpositionTable[(player << 64) | opponent]
                # We use complex numbers as 2-tuples for memory efficiency. 
                # Real: previous stored depth, Imag: previous stored flag
                if lookup[1].real <= depth:
                    lookupValue = lookup[0]
                    flag = lookup[1].imag
                    if flag == 1: # Exact
                        return lookupValue
                    elif flag == 2: # Lower bound
                        alpha = max(alpha, lookupValue)
                    elif flag == 3: # Upper bound
                        beta = min(beta, lookupValue)

                    if alpha >= beta:
                        return lookupValue
            except:
                pass

        moves = getMoves(player, opponent)

        isOpponent = False
        if not moves: # If no moves available
            moves = getMoves(opponent, player)
            if moves: # If opponent has moves.. "go down" a ply in the current recursion
                if depth == 1:
                    value = evalBoard(player, opponent)
                    # Store in transposition table every time we return 
                    tranpositionTable[(player << 64) | opponent] = \
                        (value, depth + (3j if (value <= alpha) else (2j if value >= beta else 1j)) )
                    return value
                isOpponent = True
                player, opponent = opponent, player # Swap
                alpha = -beta
                beta = -alpha
                depth -= 1
            else:
                value = finalBoardValue(player, opponent)
                # Store in transposition table every time we return 
                tranpositionTable[(player << 64) | opponent] = \
                    (value, depth + (3j if (value <= alpha) else (2j if value >= beta else 1j)) )
                return value

        nextBoards = [(opponent ^ rev, player ^ (move | rev)) for move, rev in moves]
        nextBoardEvalValues = evalBoardsMoveOrderingVectorized(nextBoards)

        sortedMoves = zip(nextBoardEvalValues, moves, nextBoards)
        sortedMoves.sort()

        b = beta
        a = alpha

        bestMove = isRoot and sortedMoves[0][1][0]
        i = 0 # is first iteration
        for next in sortedMoves:
            nextPlayer, nextOpponent = next[2]
            # This will be a null window search after the 1st iteration... 
            t = -reversiABNegaScout(nextPlayer, nextOpponent, depth-1, depthCounters, -b, -alpha, False, tranpositionTable)
            # If the principle variation has been refuted. (i.e. not first iteration and value is within bounds)
            if i and a < t < beta:
                # Retry with a full window
                t = -reversiABNegaScout(nextPlayer, nextOpponent, depth-1, depthCounters, -beta, -alpha, False, tranpositionTable)
            if t > alpha:
                bestMove = isRoot and next[1][0]
                alpha = t
            if alpha >= beta:
                break
            i = 1
            b = alpha + 1
        
        # Store in transposition table every time we return 
        tranpositionTable[(player << 64) | opponent] = \
            (alpha, depth + (3j if (alpha <= a) else (2j if alpha >= beta else 1j)) )

        # Prevent exceed memory
        # Emprical tests show that a simple deletion of first 20% of keys performs way
        # better than random or LRU deletion as Python is just too overheaded for complex custom cache handling
        if tranpositionTable.__len__() > 50000:
            for k in tranpositionTable.keys()[:tranpositionTable.__len__()/5]:
                del tranpositionTable[k]

        # If we have "went down" a ply because player has no move, negate back the alpha
        if isOpponent:  
            alpha = -alpha

        return (bestMove, alpha) if isRoot else alpha

# Create a new depth counter
def getNewDepthCounters(depth):
    depthCounters = [0] * (depth + 1)
    depthCounters[depth] = 1
    return depthCounters

# We need to return two different branching factors, for player and for opponent
# When they are highly different (when one side has much better mobility), 
# it can affect the estimate's accuracy.
def getAverageBranchingFactors(previousDepthCounters):
        depthCountersLen = len(previousDepthCounters)
        playerBranchingFactor = 0
        playerLevels = 0
        opponentBranchingFactor = 0
        opponentLevels = 0
        for x in xrange(0, depthCountersLen, 2):
            try:
                playerBranchingFactor += previousDepthCounters[x] / float(previousDepthCounters[x+1])
                playerLevels += 1
            except:
                pass
        for x in xrange(1, depthCountersLen, 2):
            try:
                opponentBranchingFactor += previousDepthCounters[x] / float(previousDepthCounters[x+1])
                opponentLevels += 1
            except:
                pass
        if playerLevels > 0: 
            playerBranchingFactor /= playerLevels
        if opponentLevels > 0 : 
            opponentBranchingFactor /= opponentLevels
        return playerBranchingFactor, opponentBranchingFactor

# How deep should we search before exceeding the single search time limit?
def getMaxSuggestedDepthForTime(previousDepthCounters, previousSearchTime, searchTimeLimit):
    totalNodes = sum(previousDepthCounters)
    if totalNodes <= 0:
        return 6
    timePerNode = abs(float(previousSearchTime) / totalNodes)
    branchingFactors = getAverageBranchingFactors(previousDepthCounters)
    suggestedDepth = -1
    expectedTime = 0
    turn = 0
    currentLevelNodeCount = 1
    for x in xrange(61):
        expectedTime += currentLevelNodeCount * timePerNode
        currentLevelNodeCount *= branchingFactors[turn]
        if expectedTime > searchTimeLimit:
            suggestedDepth -= 1
            break
        else:
            suggestedDepth += 1
            turn = 0 if turn else 1
    return max(suggestedDepth, 0)

# How deep should we search to maximize the remaining time?
def getSuggestedDepthForCompetition(midGameTimeLeft, gameTimeLeft, endGameNumEmpties, 
    minSearchDepth, player, opponent, previousDepthCounters = None, previousSearchTime = None, 
    forceEndGame = False):

    numEmptiesLeft = getNumEmptiesLeft(player, opponent)

    if numEmptiesLeft > endGameNumEmpties: # Still midgame

        if previousDepthCounters == None or previousSearchTime == None: # not first search
            testSearchDepth = 6
            previousDepthCounters = getNewDepthCounters(testSearchDepth)
            timeStart = time.time()
            # Just do a shallow search...
            reversiABNegaScout(player, opponent, testSearchDepth, previousDepthCounters) 
            previousSearchTime = time.time() - timeStart
            midGameTimeLeft -= previousSearchTime

        numMidGameEmptiesLeft = numEmptiesLeft - endGameNumEmpties
        selfEmptiesLeft = numMidGameEmptiesLeft / 2

        if numMidGameEmptiesLeft & 1: # if odd number of empties left in midgame
            selfEmptiesLeft += 1

        timeForSearch = midGameTimeLeft / float(selfEmptiesLeft) # Divide evenly...
        return max(minSearchDepth, 
            getMaxSuggestedDepthForTime(previousDepthCounters, previousSearchTime, timeForSearch) )
    else:
        if forceEndGame:
            return 61
        # If we have previous search stats, try see if we can safely launch the endgame search
        if previousDepthCounters != None and previousSearchTime != None: 
            # Check if capable of searching to endgame...
            timeForSearch = gameTimeLeft * 0.7 # Assume that end game takes 70% of remaining time
            maxSuggestedDepth = getMaxSuggestedDepthForTime(previousDepthCounters, previousSearchTime, timeForSearch)
            if maxSuggestedDepth >= endGameNumEmpties:
                return 61 # Proceed to endgame
            else: # Do a pre-end game search
                return max(minSearchDepth, 
                    getMaxSuggestedDepthForTime(previousDepthCounters, previousSearchTime, timeForSearch * 0.7))
        else: # We were already confident to proceed with endgame
            return 61
