import structure
import sys

class Move:
    def __init__(self, x, y, edgeType):
        self.x = x
        self.y = y
        self.edgeType = edgeType

    @staticmethod
    def stringToMove(string):
        string = string.replace("(", "")
        string = string.replace(")", "").strip("\n")
        x, y, edgeType = string.split(",")
        x = int(x)
        y = int(y)
        edgeType = int(edgeType)
        return Move(x, y, edgeType)

    def __eq__(self, other):
        if other is None and self is not None:
            return False
        if other is not None and self is None:
            return False
        if self is None and other is None:
            return True
        if self.x == other.x and \
           self.y == other.y and \
           self.edgeType == other.edgeType:
            return True

        neighborX, neighborY = structure.getNeighborCoordinates(self.x, self.y, self.edgeType)

        if neighborX == other.x and \
           neighborY == other.y and \
           structure.oppositeEdge(self.edgeType) == other.edgeType:
            return True

        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        if self.edgeType == structure.Edge.LEFT or \
                self.edgeType == structure.Edge.TOP:
            return hash((self.x, self.y, self.edgeType))
        
        neighborX, neighborY = \
                structure.getNeighborCoordinates(self.x, self.y, self.edgeType)
        return hash((neighborX, neighborY, structure.oppositeEdge(self.edgeType))) 

    def __str__(self):
        return "(%d, %d), %s" % (self.x, self.y, self.edgeType)
    
    def __repr__(self):
        return self.__str__()
