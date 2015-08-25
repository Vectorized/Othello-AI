from b78 import *

def getBoard(opening):
    player, opponent = getStartBoard()
    currentColor = 'B'

    for sq in chunks(opening, 2):
        validMoves = getMoves(player, opponent)
        move, rev = {bitToLetterCoors[m[0]]:m for m in validMoves}[''.join(sq).upper()]
        player, opponent = getPut(player, opponent, move, rev)
        # Swap!
        player, opponent = opponent, player 
        currentColor = {'B':'W', 'W':'B'}[currentColor]

    return player, opponent, currentColor

def getMaxValues(l):
    l = sorted(l)[::-1]
    return [e for e in l if e[0]==l[0][0]]

uniqueAndBestMoves = {}

def addscore(opening, scores):
    player, opponent, currentColor = getBoard(opening)
    validMoves = getMoves(player, opponent)
    bestMoves = getMaxValues(zip(scores, sorted(bitToLetterCoors[m[0]] for m in validMoves)))
    combined = (player << 128) | opponent
    unique, symmetryIndex = getUniqueBoard(combined)
    bitMoves = [getSymmetricMoveSingle(letterCoorsToBit[m[1]], symmetryIndex) for m in bestMoves]

    if bitToLetterCoors[getSymmetricMoveSingleInverse(bitMoves[0], symmetryIndex)] != bestMoves[0][1]:
        print bitToLetterCoors[getSymmetricMoveSingleInverse(bitMoves[0], symmetryIndex)], bestMoves[0][1], symmetryIndex
    uniqueAndBestMoves[hex(unique)] = tuple(map(hex, bitMoves))

# Indicates opening name from expanded list
addscore('',[0,0,0,0]); # Starting Position
addscore('c4',[0,-6,0]); # Initial Move
#  Diagonal Openings
addscore('c4c3',[-11,0,-6,-7]); # Diagonal Opening
addscore('c4c3c2',[-26,3,13,5,1,6]);
addscore('c4c3d3',[0,0]);
addscore('c4c3d3c5',[-16,-4,0,-4,-4,-4,0,-5,-4]);
addscore('c4c3d3c5b2',[10,18,17,16,19.9,19,20]); # X-square Opening
addscore('c4c3d3c5b3',[-12,-29,-4,-5,-4,-1,-1,4]); # Snake/Peasant
addscore('c4c3d3c5b3e3',[-1,-3,0,-5,-0.1,-6,-13]); # Stuck Peasant *
addscore('c4c3d3c5b3e3b5',[-14,-5,-7,-26,-3,1,0]); # *
addscore('c4c3d3c5b3e3b5c2',[-5,-6,-2,-1,-8]); # Peasant Cannibal *
addscore('c4c3d3c5b3e3d6',[-13,-6,-20,-7,0,-8,-4,-1,-7]); # Crosswise Peasant *
addscore('c4c3d3c5b3e3d6c6',[-2,0,-7,-11,-4,-10,-8,-10,-5,-7]); # *
addscore('c4c3d3c5b3e3d6c6b5',[-19,-9,-8,-8,-30,0,-13,-6,-2,-8,-1,-7]); # *
addscore('c4c3d3c5b3e3d6c6b5b4',[-9.1,-5.7,-3.3,-0.2,-3.4,0.0,-6.6,-5.6,-17.9,-3.7]); # * Example of scores all to 1 decimal place
addscore('c4c3d3c5b3e3d6c6b5b4c7',[-0.2,-5,-4,-26,-4,-24,-24,-5,-4,-0.1,-1]); # Peasant Shibata *
addscore('c4c3d3c5b3e3d6c6b5b4e6',[-10,-1,-6,-27,-7,-5,-2,-6,0,-16,-13]); # *
addscore('c4c3d3c5b3e3d6c6b5b4e6d7',[-4,-5,-3,-3,-0.1,-8,-20,-10,0,-3,-5,-4]); # *
addscore('c4c3d3c5b3e3d6c6b5b4e6d7f4',[-11,-9,-4,-4,-28,-0.2,-0.1,-3,-5,-3,-10,-6,-5,-9,-9,-9]); # Peasant Ralle *
addscore('c4c3d3c5b3e3d6e6',[-4,1,-8,-7,-9,-6,-8,-9,-15,-17]); # *
addscore('c4c3d3c5b3e3d6e6b4',[-16,-5,-6,-21,-3,4,1,1,-0.1,5,-0.1]); # Peasant Kitajima *
addscore('c4c3d3c5b3e3d6e6b5',[-16,-8,-4,-25,-2,-7,-1.1,-5,-3,-1,-2]); # *
addscore('c4c3d3c5b3e3d6e6b5c6',[1,-10,-13,-6,-2,-5,-16,-11,-11]); # *
addscore('c4c3d3c5b3e3d6e6b5c6b6',[-20,-8,-3,-5,-1.2,-11,-26,-1.3,-21,-1.4]); # Peasant Taniguchi *
addscore('c4c3d3c5b3f3',[0,-2,-2,1,-8,-5,-0.1,-9,-9]); # Lysons
addscore('c4c3d3c5b3f3b4',[-18,-12,-4,-30,-10,-8,0]); # Peasant Traneau *
addscore('c4c3d3c5b3f3b5',[-19,-6,-30,0,-10,-7,2]);
addscore('c4c3d3c5b3f3b6',[-17,-29,-5,-7,2,-3,-9]);
addscore('c4c3d3c5b3f3f4',[-15,-26,-1,-7,-6,-1,-0.1,-6,-6]); # Nordic Peasant *
addscore('c4c3d3c5b3f4',[-4,-4.1,-5,-11,-9,-10]); # Right-sided Peasant *
addscore('c4c3d3c5b3f4b5',[-12,-3,-30,4,-7,-3]);
addscore('c4c3d3c5b3f4b5b4',[-4,-4.1,-4.1,-4,-13,-4.1]);
addscore('c4c3d3c5b3f4b5b4a5',[-31,-1,-8,1,-19,-8,-9,-4]); # Peasant 9 in the Edge *
addscore('c4c3d3c5b3f4b5b4a5a3',[1,0,-5,-14,-3]); # *
addscore('c4c3d3c5b3f4b5b4a5a3c6',[-14,-38,-6,-27,-10,-8,-1,-10]); # Peasant Continuation 1 *
addscore('c4c3d3c5b3f4b5b4a5a3d6',[-7,-12,-29,-7,-0.1,-2,-18,-2,-14,-4,-7,-13]); # Danish Peasant *
addscore('c4c3d3c5b3f4b5b4a5a6',[-3,-3,-1,-9,-8,-30,-6,-14]); # *
addscore('c4c3d3c5b3f4b5b4a5a6c6',[-25,1,-35,-1,-33,-15,-14,-8,-14]); # *
addscore('c4c3d3c5b3f4b5b4a5a6c6a4',[-1,-16,-2,-6,-13,-17,-25,-8]); # Peasant Nail *
addscore('c4c3d3c5b3f4b5b4a5a6c6b6',[-1,-9,-18,-7,1,-13,-17,-11,-5,-39]); # *
addscore('c4c3d3c5b3f4b5b4a5a6c6b6a4',[-63,1,-33,-46,-25,-31,-24,-11,-18]); # *
addscore('c4c3d3c5b3f4b5b4a5a6c6b6a4a3',[-34,-1,-3,-10,-19,-10,-28]); # *
addscore('c4c3d3c5b3f4b5b4a5a6c6b6a4a3d6',[-31,-29,-7,-7,1,-1,-4,-16,-2,-4]); # Peasant Continuation 2 *
addscore('c4c3d3c5b3f4b5b4a5a6c6b6d6',[-7,-35,-27,-10,-3,-1,-9,-8,-2]); # Milan Peasant *
addscore('c4c3d3c5b3f4b5b4c6',[-17,-4,-32,-7,-30,-16,-16,4]);
addscore('c4c3d3c5b3f4b5b4c6d6',[-4.1,-4.1,-9,-4,-6,-4,-9,-13]);
addscore('c4c3d3c5b3f4b5b4c6d6a4',[-7,-7,-2,-20,-2,-18,-9,2,-3]); # Classic Peasant or 11 in the Edge *
addscore('c4c3d3c5b3f4b5b4d6',[-12,-8,-5,-23,-7,-4,2,-13,-1,-5,-5,-5,-9]); # Peasant Berner *
addscore('c4c3d3c5b3f4b5b4c6d6f5',[-22,4,-1,-4]); # Pyramid/Checkerboarding Peasant
addscore('c4c3d3c5b4',[-5,-8,-4,0,-3,-5]); # Heath/Tobidashi 'Jumping Out'
addscore('c4c3d3c5b4b3',[-1,-33,2,-5,-6,0,-9,-6,-7]); # Heath of Aviodance *
addscore('c4c3d3c5b4b3b5',[-4,-10,-14,-2,-7,-6]); # *
addscore('c4c3d3c5b4b3b5d2',[-12,-30,-1,2,0,-5,-2,-9,-11]); # *
addscore('c4c3d3c5b4b3b5d2c6',[-2,-12,-4,-10,-14,-5,-4,-12,-7,-7]); # Madagascar Heath of Aviodance *
addscore('c4c3d3c5b4d2',[0,-4,0,-5,-4,-7]);
addscore('c4c3d3c5b4d2c2',[-3,0,-9,-36,-3,-6,-1,-2,-2]); # Classic Heath
addscore('c4c3d3c5b4d2c2a4',[-13,-1,-4,-1,0,-4,-4,-0.1,-5]); # Heath at the edge *
addscore('c4c3d3c5b4d2c2a4b5',[-3,-34,1,-9,-9,-7,-9,-2,-4]); # Diagonal Heath at the edge *
addscore('c4c3d3c5b4d2c2a4b5a5',[-4,-9,-6,3,-9,-9,-15,-9]); # *
addscore('c4c3d3c5b4d2c2a4b5a5d6',[-36,-11,-17,-15,-9,-4,-14,-8]); # *
addscore('c4c3d3c5b4d2c2a4b5a5d6e3',[-12,2.2,-0.1,-2,-1,-6,-1,-4,-6,2.1]); # Diagonal Heath on the edge *
addscore('c4c3d3c5b4d2c2a4b5b3',[-10,-3,-31,-11,-2,-1,-7,-11,-13,-22,-12]); # *
addscore('c4c3d3c5b4d2c2a4b5b3d6',[-1,-3,-25,-6,-1,1,-3,-7,-15,-7,-6,-7,-6,-1]); # Diagonal Heath on the pre-edge *
addscore('c4c3d3c5b4d2c2a4b5b3d6a5',[-11,-20,-6,-6,-4,-6,-8,-7,-6,-8,-10,-9]); # Heath Kawazoe *
addscore('c4c3d3c5b4d2c2a4b5b3d6c1',[-13,-10,-37,-32,1,-3,-7,-8,-10,-9]); # Heath Variant 56 *
addscore('c4c3d3c5b4d2c2a4b5b3d6c6',[-9,-2,-7,-1,-1.1,-21,-3,-2,-5,-2,-6,-6,-8,-6]); # Heath Ka *
addscore('c4c3d3c5b4d2c2a4b5b3d6e6',[-8,-2,-28,-1,4,-7,-9,-7,-18,-2,-10,-16]); # *
addscore('c4c3d3c5b4d2c2a4b5b3d6e6c6',[-7.4,-37,-14,-8,-11,-28,-6.7,-11,-13]); # Heath Shaman Delayed (Inversion) *
addscore('c4c3d3c5b4d2c2a4d6',[-35,-11,-9,-16,-8,-5,1,-10,-10]); # Median Heath at the edge *
addscore('c4c3d3c5b4d2c2a4d6e6',[-7,-13,-0.9,-1.1,-4,-8,-10,-11,-17,-7,-13]); # *
addscore('c4c3d3c5b4d2c2a4d6e6b5',[1,-30,-8,-5,-16,-8,-6,-3,-4,-6,-2,-3]); # *
addscore('c4c3d3c5b4d2c2a4d6e6b5a5',[-12,-1,-11,-2,-13,-14,-14,-17,-9,-14,-3]); # *
addscore('c4c3d3c5b4d2c2a4d6e6b5a5a6',[-0.2,-35,1,-2,-19,-11,-19,-14,-8,-18,-2,-11]); # *
addscore('c4c3d3c5b4d2c2a4d6e6b5a5b6',[-37,-7,-29,8,-12,-6,-10,-9,-9,-1,-5]); # Heath Scorpion *

#  Expanded scores to here



#  Current working above

addscore('c4c3d3c5b4d2c2e3',[1,-2,-2,-1,-2,-2,-2,-0.1,-4,-2]);
addscore('c4c3d3c5b4d2c2f4',[2,-2,-6,-7,-8,-7,-8,-9,-13]);
addscore('c4c3d3c5b4d2c2f4d6',[-10,-5,-18,-34,-7,4,-6,-9]);
addscore('c4c3d3c5b4d2c2f4d6c6',[-9,-11,-14,-15,-18,-6,-11,-13,-18,-19]);
addscore('c4c3d3c5b4d2c2f4d6c6f5',[-2,-1,-25,3,-3,1,9,1,6]);
addscore('c4c3d3c5b4d2c2f4d6c6f5e6',[-36,-23,-20,-14,-19,-21,-18,-12,-16,-13,-12.1]);
addscore('c4c3d3c5b4d2c2f4d6c6f5e6f7',[6,-1,3,-17,5,7,13]); # Mimura Variation II
addscore('c4c3d3c5b4d2d6',[-10,-9,0,-4,-5,-3,-9,-12,-4,-5,-4,-5]); # Heath-Bat
addscore('c4c3d3c5b4d2d6b3',[-30,-1,-0.1,-14,-14,0,0,-0.1,-7]); # Diagonal Heath Comp'Oth *
addscore('c4c3d3c5b4d2e2',[-4,-10,-5,4,-3,-8,-9,-8]); # Iwasaki Variation
addscore('c4c3d3c5b4e3',[0,0,0,0,3,0,0]); # Heath-Chimney 'Mass-Turning'
addscore('c4c3d3c5b4e3f4',[-4,-7,-2,-0.1,1,1,-8,-7]); # Last + slice = Chimney + slice
addscore('c4c3d3c5b5',[-11,-2,4,-4,-2]); # Raccoon Dog
addscore('c4c3d3c5b6',[-4,2,0,-0.1,4,-1,-0.1]); # Rocket
addscore('c4c3d3c5b6c6',[-25,-2.1,-2,-3,-26,-15,-3,-6]);
addscore('c4c3d3c5b6c6b5',[-2,1,3,-7,-0.1,-3,-3,-0.1]); # Hamilton
addscore('c4c3d3c5b6e3',[-25,-6,-10,-7,-4,-9,-4.1,-15,-7]); # Lollipop
addscore('c4c3d3c5c6',[-7,-1,-4,-4,4]);
addscore('c4c3d3c5d6',[-8,-4,0,-4,-9,-0.1]); # Cow
addscore('c4c3d3c5d6e3',[-0.1,-4,0,0,0,-4,0]); # Chimney
addscore('c4c3d3c5d6e3d2',[-4,-2,1,-8,-7,-0.1,1,-7]); # Last + slice = Heath-Chimney + slice
addscore('c4c3d3c5d6e3f3',[-8,-11,-4,-9,1,-2,-7]); # Chimney+
addscore('c4c3d3c5d6e3f3f4',[-13,-4,-4,-1,-6,-13]); # Chimney++ = Cow+++
addscore('c4c3d3c5d6f4',[-4,-3,-4,-0.1,0,-8]);
addscore('c4c3d3c5d6f4b4',[-10,-6,-12,3,-4,0,-9,-4,-9,-7,-1,-1]); # Cow Bat/Bat/Cambridge
addscore('c4c3d3c5d6f4b4b6',[-4,-3,-5,-3.1,-3.1,-8,-3.1]);
addscore('c4c3d3c5d6f4b4b6b5',[-10,-22,-14,-3,3,-6,-4,-10,-2]);
addscore('c4c3d3c5d6f4b4b6b5c6',[-10,-3.1,-28,-5,-3,-3.1,-16,-16]);
addscore('c4c3d3c5d6f4b4b6b5c6b3',[-22,-5,-17,-9,-3,-30,-14,-2,-11,-5,-8,3,-7]); # Bat (Piau Continuation 2)
addscore('c4c3d3c5d6f4b4b6b5c6f5',[-9,-2,0,-10,-6,-2,-6,-4,3,-2,0,-6]); # Melnikov/Bat (Piau Continuation 1)
addscore('c4c3d3c5d6f4b4c6',[0,-2,-7,-5,-3,-13,-12]);
addscore('c4c3d3c5d6f4b4c6b5',[-7,-15,-15,2,-11,-11,-12,-11,-5,-6,-14]);
addscore('c4c3d3c5d6f4b4c6b5b3',[-13,-26,-2.1,-2,-7,-9,-14,-10]);
addscore('c4c3d3c5d6f4b4c6b5b3b6',[-6,-8,-13,-7,-21,-30,-2,-17,-5,-10,-5,2,-8]);
addscore('c4c3d3c5d6f4b4c6b5b3b6e3',[-27,-2,-14,-11,-6,-12,-10,-14,-13]);
addscore('c4c3d3c5d6f4b4c6b5b3b6e3c2',[2,-3,-0.1,-14,-16,-25,-38,-13,-13,-8]);
addscore('c4c3d3c5d6f4b4c6b5b3b6e3c2a4',[-10,-4,-26,-2,-5,-8,-14,-14,-13,-22]);
addscore('c4c3d3c5d6f4b4c6b5b3b6e3c2a4a5',[4,-33,-21,-29,-30,-26,-27,-17,-29]);
addscore('c4c3d3c5d6f4b4c6b5b3b6e3c2a4a5a6',[-15,-19,-6,-16,-15,-15,-15,-35,-19]);
addscore('c4c3d3c5d6f4b4c6b5b3b6e3c2a4a5a6d2',[0,-12,-18,-31,-5,-7,1,2,-4,-1,-11]); # Bat (Kling Continuation)
addscore('c4c3d3c5d6f4b4e3',[1,-2,-11,-10,-5,-6,-16,-10]);
addscore('c4c3d3c5d6f4b4e3b3',[-1,-3,-4,-7,-7,-2,-2,-10]); # Bat (Kling Alternative)
addscore('c4c3d3c5d6f4f3',[-8,-6,-9,-7,1,-1,-8,-6]); # Cow++
addscore('c4c3d3c5d6f4f3e3',[-13,-4,-4,-1,-6,-13]); # Cow+++ = Chimney ++
addscore('c4c3d3c5d6f4f5',[-12,-0.1,-4,-1,-2,-1,-3,-9,-7]); # Rose-v-Toth
addscore('c4c3d3c5d6f4f5d2',[-30,-8,-9,-2,-5,-13,0,-1,-1]); # Tanida
addscore('c4c3d3c5d6f4f5d2b5',[-7,1.9,2,-12,-8,-2,-12,-4]); # Aircraft/Feldborg
addscore('c4c3d3c5d6f4f5d2g4',[1,-1,-1,-7,-8,-5,-8]);
addscore('c4c3d3c5d6f4f5d2g4d7',[-25,-5,-6,-9,-2,-1]); # Sailboat
addscore('c4c3d3c5d6f4f5e6c6',[-10,-9,-6,-1,-7,-10,-4,-3,-9,-6]);
addscore('c4c3d3c5d6f4f5e6c6d7',[-22,-6,1,0,-11,-7,-7,-4,-1,-1,-5,-0.1,-9,-8]); # Maruoka
addscore('c4c3d3c5d6f4f5e6',[-27,-13,-7,-9,1,0,-2,-10,0,-15,-14]);
addscore('c4c3d3c5d6f4f5e6f6',[0,-5,-5,-7,-8,-5,-4,-15,-7,-21]); # Landau
addscore('c4c3d3c5e6',[2,-0.1,5,1,-1,-0.1,-6,-6]);
addscore('c4c3d3c5f6',[-2,4,1,-2,-5,-0.1,-19]); # Buffalo/Kenichi Variation
addscore('c4c3d3c5f6e2',[-27,-7,-4.1,-4,-12,-4,-4.1,-4.1]); # Ishii Unstuck *
addscore('c4c3d3c5f6e2c6',[-5,-2,4,-2,-5,-7,-27]); # Maruoka Buffalo
addscore('c4c3d3c5f6e3',[-27,-4,-13,-7,-1,-17]); # Stuck Ishii *
addscore('c4c3d3c5f6e3c6',[-4,-1,-6,0,1,-26]);
addscore('c4c3d3c5f6e3c6f5',[-19,-13,-3,-1]); # Ishii Cannibal *
addscore('c4c3d3c5f6e3c6f5f4',[-20,-3,0,-7,1,-7,-25]);
addscore('c4c3d3c5f6e3c6f5f4g5',[-10,-2,-1,-1]); # Tanida Buffalo
addscore('c4c3d3c5f6f5',[-27,-7,-2,-8,-7,-9,-7,0,-10,-14]); # Hokuriku Buffalo
addscore('c4c3e6',[6,3,-1,2,0]);
addscore('c4c3e6c5',[-27,-14,-3.1,-13,-3]); # Wing Variation
addscore('c4c3f5',[7,4,-3,-2,0]);
addscore('c4c3f5b4',[-8,-32,-14,-7]);
addscore('c4c3f5c5',[-30,-12,-7,-15,-8]); # Semi-Wing Variation

#  Parallel Openings
addscore('c4c5',[-11,0,6,-2,-8]); # Parallel Opening
addscore('c4c5b6',[1,3,5,9,3,3]);
addscore('c4c5c6',[-0.2,-1,-0.1]);
addscore('c4c5d6',[-6,-6.1,-6.1,-6.1]);
addscore('c4c5d6c3',[1,-6,-5,0,6,-3,1]);
addscore('c4c5d6c3e6',[-6,-10,-6,-6.1,-8,-8]);
addscore('c4c5d6c7',[3,-1,-0.1,6,0,-1,-2]);
addscore('c4c5d6c7d7',[-6,-10,-8]);
addscore('c4c5d6e3',[-1,2,6,-1,-1,-4,-2]);
addscore('c4c5d6e3c6',[-12,-6,-10,-27,-13,-8]);
addscore('c4c5d6e3d3',[-3,-6,-0.1,-5,-13,-12]);
addscore('c4c5d6e7',[-2,-1,3,6,-2,-2,-1]);
addscore('c4c5d6e7d7',[-6,-8,-12]);
addscore('c4c5e6',[3,-4,1]);
addscore('c4c5e6c3',[-26,-4,-5,-12,-7]);
addscore('c4c5f6',[2,3,6,5,0,4]);
addscore('c4c5f6d3',[-12,-15,-12,-8,-15,-16]);

#  Perpendicular Openings    
addscore('c4e3',[-8,-4,-4,0,0]); # Perpendicular Opening
addscore('c4e3f2',[1,2,7,8,1]);
addscore('c4e3f2',[1,2,7,8,1]);
addscore('c4e3f2c6',[-11,-8,-10,-11]);
addscore('c4e3f3',[-1,4,-5]); # Collay *
addscore('c4e3f3c5',[-9,-4,-13,-8]);
addscore('c4e3f4',[-6,4,-7,-5]); # Fishhook
addscore('c4e3f4c5',[-4.1,-8,-4,-6,-4]);
addscore('c4e3f4c5c6',[-4,4,-4,-7,3,-9,-7,-8]);
addscore('c4e3f4c5d6',[-5,-4,-4,-8,-5,-6,4,-3,-5,-9,-9]);
addscore('c4e3f4c5d6e6',[-7,5,-7,4.9,-6,-5]); # Mimura
addscore('c4e3f4c5d6f3',[-6,-15,-5,-4.1,-11,-4.1,-4,-4.1,-8]);
addscore('c4e3f4c5d6f3c6',[3,4,0,-9,-25,-2,1,-10,1,-9,-6]); # Shaman/Danish
addscore('c4e3f4c5d6f3d3',[0,2,4,-1,-3,-5,-8,-3,1]); # Inoue
addscore('c4e3f4c5d6f3d3c3',[-29,-6,-9,-4,-6,-11,-4.1,-14,-24]); # Iago
addscore('c4e3f4c5d6f3e2',[1,0,3.9,-5,4,0,-0.1,3,2,3,3]); # Bhagat
addscore('c4e3f4c5d6f3e6',[-1,4,-1,-2,-11,-5,-3,-8,-9]);
addscore('c4e3f4c5d6f3e6c3',[-25,-6,-12,-6,-16,-4,-12,-8,-21]);
addscore('c4e3f4c5d6f3e6c3d3',[-2,-2,4,-13,-11,-3,-11,-2,-7]);
addscore('c4e3f4c5d6f3e6c3d3e2',[-23,-10,-5,-4,-4,-4.1,-12,-7,-21]); # Rose
addscore('c4e3f4c5d6f3e6c3d3e2b5',[-3,0,0,-7,-9,4,-2,-5,-5,-5]); # Flat
addscore('c4e3f4c5d6f3e6c3d3e2b5f5',[-23,-4.1,-4,-10,-4.1,-14,-19,-14,-24,-6,-10,-5]); # Rotating Flat
addscore('c4e3f4c5d6f3e6c3d3e2b5f5b3',[1,-14,-2,4,-13,-8,-11,-7,-9,0]); # Murakami Variation
addscore('c4e3f4c5d6f3e6c3d3e2b5f5b4',[-6,-24,-4,-15,-6,-17,-8,-11,4]);
addscore('c4e3f4c5d6f3e6c3d3e2b5f5b4f6',[-4,-13,-20,-12,-10,-28,-7,-17,-4.1,-4.1]);
addscore('c4e3f4c5d6f3e6c3d3e2b5f5b4f6c2',[-14,-12,-10,-8,-15,1,-5,-2,-6,-3,4]);
addscore('c4e3f4c5d6f3e6c3d3e2b5f5b4f6c2e7',[-4.1,-16,-12,-5,-4,-25,-23,-6,-10,-26,-24]);
addscore('c4e3f4c5d6f3e6c3d3e2b5f5b4f6c2e7d2',[-19,-12,-14,-11,-18,-36,-6,-5,-4,-4,4]);
addscore('c4e3f4c5d6f3e6c3d3e2b5f5b4f6c2e7d2c7',[-4.1,-4,-6,-15,-8,-23,-10,-11,-15,-11,-26]); # Rotating Flat (Kling Continuation)
addscore('c4e3f4c5d6f3e6c3d3e2b6',[-13,-3,-8,-12,4,-5,-5,-3,-5]);
addscore('c4e3f4c5d6f3e6c3d3e2b6f5',[-20,-4.1,-4,-4.1,-4.1,-14,-13,-25,-10,-5,-4.1]); # Rose-Birth
addscore('c4e3f4c5d6f3e6c3d3e2b6f5b4',[-8,-3,-24,-14,-8,-14,-7,-10,4]);
addscore('c4e3f4c5d6f3e6c3d3e2b6f5b4f6',[-4.1,-16,-18,-14,-8,-28,-11,-17,-4.1,-4]);
addscore('c4e3f4c5d6f3e6c3d3e2b6f5b4f6g5',[-1,1,-14,1,-8,1,1,0,4,-1,1]);
addscore('c4e3f4c5d6f3e6c3d3e2b6f5b4f6g5d7',[-18,-11,-2,-8,-9,-9,-13,-7,-11,-10,-6,-7,-3,-1,-20]); # Brightstein
addscore('c4e3f4c5d6f3e6c3d3e2b6f5b4f6g5g6',[-21,-6,-18,-21,-5,-14,-12,-30,-10,-4,-37,-7]);
addscore('c4e3f4c5d6f3e6c3d3e2b6f5g5',[-9,-1,-8,-4,-5,1,-5,4,-2]); # Rose-Birdie/Rose-Tamenori
addscore('c4e3f4c5d6f3e6c3d3e2b6f5g5f6',[-6,-11,-11,-15,-1,-9,-22,-9,-2,-2]); # Rose-Tamenori-Kling
addscore('c4e3f4c5d6f3e6c3d3e2d2',[-0.1,2,1,-12,4,-5,1,-10,-3]); # Greenberg/Dawg
addscore('c4e3f4c5d6f3e6c6',[-2,-1,-9,-6,-13,-9,1,-9,-12]); # Ralle
addscore('c4e3f4c5d6f5',[-11,-6,-8,3,-10,-6,-3,-7]);
addscore('c4e3f4c5e6',[-0.1,-2,4,-10,2,-5,-10,-9]); # Horse
addscore('c4e3f5',[0,-4,-4,0,-4]);
addscore('c4e3f5b4',[-6,0,-10,-5,0]); # Ganglion/No-Cat
addscore('c4e3f5b4f3',[-4,-4,0,-5,-4]); # Swallow
addscore('c4e3f5b4f3f4',[-8,0,-4,0,0]);
addscore('c4e3f5b4f3f4c3',[-4,0,-8,-7,-3,-9,-2,-3,-21,-6,-4]);
addscore('c4e3f5b4f3f4e2',[-4,-11,0,-2,-2]);
addscore('c4e3f5b4f3f4e2e6',[-19,-2,-3,-2,-8,-13,-3,-2,0]);
addscore('c4e3f5b4f3f4e2e6g5',[-14,-11,0,-25,-11,-7]);
addscore('c4e3f5b4f3f4e2e6g5f6',[-19,-14,-9,0,-8,-8,-4]);
addscore('c4e3f5b4f3f4e2e6g5f6d6',[0,-4,-10,-9,-23,0,-6,-3]);
addscore('c4e3f5b4f3f4e2e6g5f6d6c6',[-17,-23,-3,-4,-7,0,-7,-2,-23]); # No-Cat (Continuation)
addscore('c4e3f5b4f3f4g3',[-2,-3,-5,0,-23,-2,-5,-4,-8]);
addscore('c4e3f5e6',[-4,-8,-5,-5,-4,0,-12]);
addscore('c4e3f5e6d3',[-4,-1,4,-2,0]); # Italian
addscore('c4e3f5e6f4',[-7,-5,4,-1,-3,0]); # Cat
addscore('c4e3f5e6f4c5',[-9,-13,-4.1,-4.1,-4,-4.1,-7,-16]);
addscore('c4e3f5e6f4c5d6',[-7,-6,-4,4,-5,-0.1,-3,-0.1,-15,-12]);
addscore('c4e3f5e6f4c5d6c6',[-5,-25,-7,-14,-11,-4,-11,-6,-4.1]);
addscore('c4e3f5e6f4c5d6c6f7',[0,2,-7,4,-0.1,-2,-3,2]);
addscore('c4e3f5e6f4c5d6c6f7f3',[-4.1,-16,-13,-18,-5,-4,-6,-11]); # Sakaguchi
addscore('c4e3f5e6f4c5d6c6f7g5',[-5,-19,-10,-11,-3,-2]);
addscore('c4e3f5e6f4c5d6c6f7g5g6',[-8,-10,-0.1,-11,1,2,-23,-22]); # Berner
addscore('c4e3f6',[-4,-4,-4,0]);
addscore('c4e3f6b4',[0,1,-4,-11,4]); # Bent Ganglion
addscore('c4e3f6e6',[-12,-16,-4,-4,0,-8]);
addscore('c4e3f6e6f5',[-11,-8,0,-7,-4,-5]); # Tiger
addscore('c4e3f6e6f5c5',[-11,-4,-10,-4,-4,-10,-17,-6,-5,0,-11]);
addscore('c4e3f6e6f5c5c3',[-6,0,-15,4,-4,-3,-16]); # Stephenson
addscore('c4e3f6e6f5c5c3b4',[-14,-5,-5,-2,0,-1,-10,-13,-9,-1,-8]); # No-Kung
addscore('c4e3f6e6f5c5c3b4d6',[-23,-5,1,-9,-9,-12,-14,-11,-16,-33]);
addscore('c4e3f6e6f5c5c3b4d6c6',[-13,-7,-2,-1,-2,-13,-2,-10]);
addscore('c4e3f6e6f5c5c3b4d6c6b5',[-1,0,-17,-3,-3,-3,1,-12,-6,-19,-25]);
addscore('c4e3f6e6f5c5c3b4d6c6b5a6',[-5,-11,-10,-2,-24,-8,-0.1,-8,-2,-6]);
addscore('c4e3f6e6f5c5c3b4d6c6b5a6b6',[-10,-16,-32,-5,3,-4,-8,-11,-4,-8,-33,-26]);
addscore('c4e3f6e6f5c5c3b4d6c6b5a6b6c7',[-7,-11,-17,-22,-16,-18,-4,-13,-17,-11,-10]); # No-Kung (Continuation)
#  addscore('C4e3F6e6F5c5C3b4D6c6B5a6B6c7d3']);
addscore('c4e3f6e6f5c5c3c6',[-4.1,-11,-17,-4,-4.1,-10,-15,-8,-4.1,-7,-9]); # Comp'Oth
addscore('c4e3f6e6f5c5c3c6d3',[-8,-4,4,-6,-7,-8,-6]);
addscore('c4e3f6e6f5c5c3c6d3d2',[-13,-26,-4,-10,-5,-6,-6,-4,-4.1,-4.1,-13]); # Scorpion
addscore('c4e3f6e6f5c5c3c6d3d2c2',[-28,-2,-1,-9,-7,4,-6,-7,-6,-22]); # Classic Scorpion
#  addscore('C4e3F6e6F5c5C3c6D3d2c2']); # Evaluate Classic Scorpion + best move   
addscore('c4e3f6e6f5c5c3c6d3d2e2',[-19,4,-2,-6,-9,-8,-6,1,-3,-3,-3,-18]); # New Scorpion
addscore('c4e3f6e6f5c5c3c6d3d2e2b3',[-4.1,-4.1,-21,-9,-30,-4.1,-4,-14,-5,-10,-8,-4,-6]);
addscore('c4e3f6e6f5c5c3c6d3d2e2b3c1',[-12,4,-7,-10,-3,-10,-10,1,-6,-7,-4,-19]);
addscore('c4e3f6e6f5c5c3c6d3d2e2b3c1c2',[-4.1,-4.1,-32,-4,-16,-8,-32,-27,-7,-4.1,-5]);
addscore('c4e3f6e6f5c5c3c6d3d2e2b3c1c2b4',[4,1,-1,-8,-12,-4,-2,-3,-11]); # Low-F.A.T.
addscore('c4e3f6e6f5c5c3c6d3d2e2b3c1c2b4a3',[-40,-15,-4,-4.1,-24,-12,-12,-23,-14,-11,-4.1,-5,-13]);
addscore('c4e3f6e6f5c5c3c6d3d2e2b3c1c2b4a3a5',[4,1,-3,-11,-3,-1,-0.1,-8]);
addscore('c4e3f6e6f5c5c3c6d3d2e2b3c1c2b4a3a5b5',[-48,-11,-4,-5,-23,-12,-24,-11,-12,-4,-4.1,-11]);
addscore('c4e3f6e6f5c5c3c6d3d2e2b3c1c2b4a3a5b5a6',[4,1,-2,-20,-16,-9,1,-4,-4,-13]);
addscore('c4e3f6e6f5c5c3c6d3d2e2b3c1c2b4a3a5b5a6a4',[-4,-17,-35,-25,-35,-31,-25,-16,-11,-27]);
addscore('c4e3f6e6f5c5c3c6d3d2e2b3c1c2b4a3a5b5a6a4a2',[-27,-2,-26,-2,-37,-10,4,-6,-3,-25]); # F.A.T. Draw
addscore('c4e3f6e6f5c5c3c6d3d2e2b3c1c2b4a3a5b5a6a4a2f4',[-25,-40,-12,-14,-14,-9,-23,-18,-4.1,-19,-4.1,-4,-4.1]);
addscore('c4e3f6e6f5c5c3c6d3d2e2b3c1c2b4a3a5b5a6a4a2f4g5',[-25,4,-6,1,-23,-3,-2,-12,-3]); # F.A.T.
#  addscore('C4e3F6e6F5c5C3c6D3d2E2b3C1c2B4a3A5b5A6a4A2f4G5']); # Evaluate F.A.T. + best move
addscore('c4e3f6e6f5c5c3c6d3d2e2b3c1c2b4a3a5b5a6b6',[-64,-1,-18,-15,-32,-23,-25,-22,-15,-2,-7]); # No-F.A.T.
#  addscore('C4e3F6e6F5c5C3c6D3d2E2b3C1c2B4a3A5b5d7']);
addscore('c4e3f6e6f5c5c3c6d6',[-1,-7,-9,4,-6]); # Lighning Bolt
#  addscore('C4e3f6e6f5c5c3c6d6g5']);
addscore('c4e3f6e6f5c5c3g5',[0,3,-4,-2,-4,0,-4]); # Kung
#  addscore('C4e3f6e6f5c5c3g5c6']);
addscore('c4e3f6e6f5c5d3',[-4,1,-6,-7,4]); # Leader's Tiger
#  addscore('C4e3f6e6f5c5d3g6']);
addscore('c4e3f6e6f5c5d6',[-1,1,4,-6,-6,-8,-7,-21]); # Brightwell
#  addscore('C4e3f6e6f5c5d6c6']);
addscore('c4e3f6e6f5c5f4',[-7,-8,-4,-3,0]);
addscore('c4e3f6e6f5c5f4g5',[-6,-2,-4,-7,-8,-7,0,-7,-2,3,-7]); # Grand Central
addscore('c4e3f6e6f5c5f4g5g4',[-8,-8,-1,-12,2,-2,-16,1,-27,-8]);
addscore('c4e3f6e6f5c5f4g5g4f3',[-7,-2,-6,-8,-5,-12,-11,-5,-3]);
addscore('c4e3f6e6f5c5f4g5g4f3c6',[-6,-10,-6,-9,-18,-4,-1,-5,-3,-1,-4,-22,-5,2,-3]);
addscore('c4e3f6e6f5c5f4g5g4f3c6d3',[-10,1,-8,-13,-19,-11,-30,-5,-12,-13]);
addscore('c4e3f6e6f5c5f4g5g4f3c6d3d6',[-1,-2,-8,-6,-22,-7,-8,-2,-2,-7,-15,-7,-8,-9]); # Ishii
addscore('c4e3f6e6f5c5f4g5g4f3c6d3d6b3',[-16,-12,1,-6,-4,-19,-19,-2,-10,-5,-1]);
addscore('c4e3f6e6f5c5f4g5g4f3c6d3d6b3c3',[-1,-10,-5,-18,-4,-5,-5,-6,-5,-3,-5,-5]);
addscore('c4e3f6e6f5c5f4g5g4f3c6d3d6b3c3b4',[-16,-14,-3,-11,-7,1,-16,-19,-14,-12,-6,-13]);
addscore('c4e3f6e6f5c5f4g5g4f3c6d3d6b3c3b4e2',[-18,-1.1,-1,-18,-2,-6,-6,-8,-8,-2,-3,-5,-13,-11,-14,-5,-5]);
addscore('c4e3f6e6f5c5f4g5g4f3c6d3d6b3c3b4e2b6',[-18,-23,-7,-6,-3,-18,-7,-1,-3,-3,-9,-6,-11,-13]); # Mainline Tiger
addscore('c4e3f6e6f5c5f4g5g4f3c6d3d6b3c3b4e2b6c2',[-18,-13,-16,-3,-4,-3,-2,-3,-4,-7,-4,-4,-15,-16,-12,-12,0,-2]);
addscore('c4e3f6e6f5c5f4g5g4f3c6h4',[-2,-11,-9,-31,-5]); # On the way to Ishii
addscore('c4e3f6e6f5c5f4g5g6',[-13,-21,-16,-3,-4,-4,-4,-5,-31,-11]); # Best from Grand Central
addscore('c4e3f6e6f5c5f4g6',[-8,-14,-5,-5,-2,-5,-4,-7,0,-24,-18]);
addscore('c4e3f6e6f5c5f4g6f7',[-4,0,0,-2,-3,0]); # Rose-Bill
addscore('c4e3f6e6f5c5f4g6f7d3',[-11,-13,-8,-19,-18,-5,0,-4,-4,-11,-9]); # Tamenori
addscore('c4e3f6e6f5c5f4g6f7d3f3',[-4,-4,-5,-4,-4,-9,-6,-8,-4,0]);
addscore('c4e3f6e6f5c5f4g6f7d6',[-11,-15,-9,-5,-15,-12,-16,0,-13,-24,-11,-18]); # Nicolet
addscore('c4e3f6e6f5c5f4g6f7d6e7',[-6,-4,-2,-14,0,-5,-1,-2]);
addscore('c4e3f6e6f5c5f4g6f7d6e7f3',[-17,-7,-4,-12,-4,-4,-10,-19,-22,-11,-15,0,-25,-12,-11,-18]);
addscore('c4e3f6e6f5c5f4g6f7g5',[-15,-9,0,-9,-5,-3,-5,-9,-9,-5,-18]); # Central Rose-Bill/Dead Draw
addscore('c4e3f6e6f5c5f4g6f7g5d6',[-17,-12,-2,-5,0,-1,-5,-10,-4,-19]);
addscore('c4e3f6e6f5c5f4g6f7g5d6d3',[-12,-12,-8,-4,-4,-12,-9,0,-4,-4,-4,-17,-11]);
addscore('c4e3f6e6f5c5f4g6f7g5d6d3f3',[0,0,-8,-1,-4,-4,-8,-5,-16]);
addscore('c4e3f6e6f5c5f4g6f7g5d6d3f3b5',[-16,-2,-14,-6,-1,0,-13,-8,-5,-5,-21,-21,-10]);
addscore('c4e3f6e6f5c5f4g6f7g5d6d3f3c3',[-21,-17,-12,-5,-9,-6,-4,0,-19,-12,-13]);
addscore('c4e3f6e6f5c5f4g6f7g5d6d3f3c3h4',[-7,-4,-4,-4,-8,-2,-8,-22,-18,0,-4]);
addscore('c4e3f6e6f5c5f4g6f7g5d6d3f3c3h4h5',[-23,-27,-18,-11,-6,-9,-1,0,-4,-14]);
addscore('c4e3f6e6f5c5f4g6f7g5d6d3f3c3h4h5g4',[-27,-2,-9,-10,-20,-6,-13,-23,-18,0]);
addscore('c4e3f6e6f5c5f4g6f7g5d6d3f3c3h4h5g4h3',[-17,-29,-18,-10,-7,-9,0,-31,-5,-11]);
addscore('c4e3f6e6f5c5f4g6f7g5d6d3f3c3h4h5g4h3e2',[-6,-2,-7,-5,-11,0,-6,-5,-1,0,-6,-17,-21]);
addscore('c4e3f6e6f5c5f4g6f7g5d6d3f3c3h4h5g4h3e2e1',[-12,-25,-5,0,0,-15,-10,-33,-8,-9]);
addscore('c4e3f6e6f5c5f4g6f7g5d6d3f3c3h4h5g4h3e2f2',[-20,-20,-19,-20,-3,0,-5,-19,-20,-33,-9,-17]); # 20-move Opening
addscore('c4e3f6e6f5c5f4g6f7g5d6d3f3c3h4h5g4h3e2f2d2',[-2,-11,0,-1,0,-4,-7,-0.1,0,0,-5,-1,-22,-19]);
addscore('c4e3f6e6f5g6',[2,1,1,5,-6,-3,-10,-22]); # Aubrey/Tanaka
addscore('c4e3f6e6f5g6e7',[-15,-5,-5,-2,-8,-8,-7,-1,-8]);
addscore('c4e3f6e6f5g6e7c5',[-3,-10,-2,-5,-1.1,-1]); # Aubrey (Feldborg Continuation)
addscore('c4e3f6e6f5g6e7c5g5',[-15,-13,-11,-2,-11,-11,-1,-6,-21,-8]);
addscore('c4e3f6e6f5g6e7c5h6',[-6,-3,-3,-4,0,-9,-18,-27]);
addscore('c4e3f6e6f5g6f3',[-13,-7,-5,-6,-5.1]);


open('opening_book.py','w').write("openingBook = " + `uniqueAndBestMoves`.replace('L','').replace("'","").replace(" ",''))


