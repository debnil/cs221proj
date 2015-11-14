import copy

def enum(**enums):
    return type('Enum', (), enums)

global Edge
Edge = enum(TOP = 0, RIGHT = 1, BOTTOM = 2, LEFT = 3)

def oppositeEdge(edgeType):
    return (edgeType + 2) % 4

def neighborCoordinates(x, y, edgeType):
    if edgeType == Edge.LEFT:
        newX = x - 1
        newY = y
    elif edgeType == Edge.RIGHT:
        newX = x + 1
        newY = y
    elif edgeType == Edge.TOP:
        newX = x
        newY = y - 1
    elif edgeType == Edge.BOTTOM:
        newX = x
        newY = y + 1
    else:
        raise ValueError("%d edge type not supported" % edgeType)
    return newX, newY

class Box():
    def __init__(self, owner = 0, \
            left = False, right = False, top = False, bottom = False):
        self.left = left # Edge is true if it's in the box
        self.right = right
        self.top = top
        self.bottom = bottom
        if owner != 0:
            assert left and right and top and bottom
        self.owner = owner # Whoever owns the box

    def rotateRight(self):
        saved = self.right
        self.right = self.top
        self.top = self.left
        self.left = self.bottom
        self.bottom = saved

    def __eq__(self, other):
        if self.left != other.left:
            return False
        if self.right != other.right:
            return False
        if self.top != other.top:
            return False
        if self.bottom != other.bottom:
            return False

    def __ne__(self, other):
        return not self == other

    def edgeCount(self):
        count = 0
        if self.left:
            count += 1
        if self.right:
            count += 1
        if self.top:
            count += 1
        if self.bottom:
            count += 1
        return count
    
    def getEdge(self, edge):
        if edge == Edge.LEFT:
            return self.left
        if edge == Edge.RIGHT:
            return self.right
        if edge == Edge.TOP:
            return self.top
        if edge == Edge.BOTTOM:
            return self.bottom

    def setEdge(self, edge, val):
        if edge == Edge.LEFT:
            self.left = val
        if edge == Edge.RIGHT:
            self.right = val
        if edge == Edge.TOP:
            self.top = val
        if edge == Edge.BOTTOM:
            self.bottom = val

    def getOwner(self):
        return self.owner

    def setOwner(self, player):
        self.owner = player

class Grid():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = []
        for _ in range(width):
            col = []
            for _ in range(height):
                col.append(Box())
            self.grid.append(col)
        print self.grid

    def getBox(self, x, y):
        if self.__inBounds(x, y):
            return self.grid[x][y]
        else:
            return None

    def removeEdge(self, x, y, edgeType):
        self.__modifyEdge(x, y, edgeType, False)

    # Adds a box and returns the number of boxes that are made by
    # adding this edge
    def addEdge(self, x, y, edgeType, player):
        boxesMade = self.__modifyEdge(x, y, edgeType, True, player)
        return boxesMade

    def __modifyEdge(self, x, y, edgeType, value, player = 0):
        boxesMade = 0
        if not self.__inBounds(x, y):
            raise ValueError("(%d, %d) out of bounds." % (x, y))
        box = self.grid[x][y]
        box.setEdge(edgeType, value)
        if box.edgeCount() == 4:
            box.setOwner(player)
            boxesMade += 1
        neighbor = self.__getNeighbor(x, y, edgeType) # modify other box sharing edge
        if neighbor is not None:
            neighbor.setEdge(oppositeEdge(edgeType), value)
            if box.edgeCount() == 4:
                box.setOwner(player)
                boxesMade += 1

    # Returns the box that shares this edge with the box at (x, y)
    # Returns None if no neighbor exists
    def __getNeighbor(self, x, y, edgeType):
        newX, newY = getNeighborCoordinates(x, y, edgeType)
        return self.getBox(newX, newY)

    def __inBounds(self, x, y):
        if x < 0:
            return False
        if x >= self.width:
            return False
        if y < 0:
            return False
        if y >= self.height:
            return False
        return True
