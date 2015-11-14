import structure
import sys

class Move:
    def __init__(self, x, y, edgeType):
        self.x = x
        self.y = y
        self.edgeType = edgeType

    def __eq__(self, other):
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
