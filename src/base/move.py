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
           oppositeEdge(self.edgeType) == other.edgeType:
            return True

        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.x, self.y, self.edgeType))

