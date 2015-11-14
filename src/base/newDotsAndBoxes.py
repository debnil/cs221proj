from structure import *
from move import *
import copy
import newUtil
import structure

class DotBoxGameState:
    def __init__(self, width, height, score, turn):
        self.width = width # Num dots wide
        self.height = height # Num dots high
        self.score = score
        self.turn = turn # -1 for player 2, 1 for player 1
        self.grid = Grid(width, height) # Grid of boxes
        self.possibleMoves = set()
        for x in range(width):
            for y in range(height):
                self.possibleMoves.add(Move(x, y, structure.Edge.LEFT))
                self.possibleMoves.add(Move(x, y, structure.Edge.TOP))

        for x in range(width):
            self.possibleMoves.add(Move(x, height - 1, structure.Edge.BOTTOM))

        for y in range(height):
            self.possibleMoves.add(Move(width - 1, y, structure.Edge.RIGHT))

    def generateSuccessor(self, x, y, edgeType):
        if Move(x, y, edgeType) not in self.possibleMoves:
            raise ValueError("(%d, %d), %s is not a valid move" % (x, y, edgeType)
        new = copy.deepcopy(self)
        boxesMade = new.grid.addEdge(x, y, edgeType, new.turn)
        if boxesMade == 0:
            new.turn *= -1
        return new
    
    def getPossibleMoves(self):
        return self.possibleMoves

    ###############################################################
    ########################## ACCESSORS ##########################
    ###############################################################

game = DotBoxGameState(2, 3, 0, 1)
newGame = game.generateSuccessor(0, 0, structure.Edge.LEFT)
newUtil.printGame(newGame)
