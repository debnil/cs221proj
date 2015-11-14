import copy

def enum(**enums):
    return type('Enum', (), enums)

global Edge
Edge = enum(TOP = 0, RIGHT = 1, BOTTOM = 2, LEFT = 3)

def oppositeEdge(edgeType):
    return (edgeType + 2) % 4

def getNeighborCoordinates(x, y, edgeType):
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
        self.left_ = left # Edge is true if it's in the box
        self.right_ = right
        self.top_ = top
        self.bottom_ = bottom
        if owner != 0:
            assert left and right and top and bottom
        self.owner_ = owner # Whoever owns the box

    def rotateRight(self):
        saved = self.right_
        self.right_ = self.top_
        self.top_ = self.left_
        self.left_ = self.bottom_
        self.bottom_ = saved

    def __eq__(self, other):
        if self.left_ != other.left:
            return False
        if self.right_ != other.right:
            return False
        if self.top_ != other.top:
            return False
        if self.bottom_ != other.bottom:
            return False

    def __ne__(self, other):
        return not self == other

    def edgeCount(self):
        count = 0
        if self.left_:
            count += 1
        if self.right_:
            count += 1
        if self.top_:
            count += 1
        if self.bottom_:
            count += 1
        return count
    
    def getEdge(self, edge):
        if edge == Edge.LEFT:
            return self.left_
        if edge == Edge.RIGHT:
            return self.right_
        if edge == Edge.TOP:
            return self.top_
        if edge == Edge.BOTTOM:
            return self.bottom_

    def setEdge(self, edge, val):
        if edge == Edge.LEFT:
            self.left_ = val
        if edge == Edge.RIGHT:
            self.right_ = val
        if edge == Edge.TOP:
            self.top_ = val
        if edge == Edge.BOTTOM:
            self.bottom_ = val

    def getOwner(self):
        return self.owner_

    def setOwner(self, player):
        self.owner_ = player

    def reset(self):
        self.left_ = False
        self.right_ = False
        self.top_ = False
        self.bottom_ = False
        self.owner_ = 0

    def __str__(self):
        return "{LEFT: %r, RIGHT: %r, TOP: %r, BOTTOM: %r}, Owner: %d" % \
                (self.left_, self.right_, self.top_, self.bottom_, self.owner_)

    def __repr__(self):
        return self.__str__()

class Grid():
    def __init__(self, width, height):
        self.width_ = width
        self.height_ = height
        self.grid_ = []
        for _ in range(width):
            col = []
            for _ in range(height):
                col.append(Box())
            self.grid_.append(col)

    def getBox(self, x, y):
        if self.__inBounds(x, y):
            return self.grid_[x][y]
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
        box = self.grid_[x][y]
        box.setEdge(edgeType, value)
        if box.edgeCount() == 4:
            box.setOwner(player)
            boxesMade += 1
        neighbor = self.__getNeighbor(x, y, edgeType) # modify other box sharing edge
        if neighbor is not None:
            neighbor.setEdge(oppositeEdge(edgeType), value)
            if neighbor.edgeCount() == 4:
                neighbor.setOwner(player)
                boxesMade += 1
        return boxesMade

    # Returns the box that shares this edge with the box at (x, y)
    # Returns None if no neighbor exists
    def __getNeighbor(self, x, y, edgeType):
        newX, newY = getNeighborCoordinates(x, y, edgeType)
        return self.getBox(newX, newY)

    def __inBounds(self, x, y):
        if x < 0:
            return False
        if x >= self.width_:
            return False
        if y < 0:
            return False
        if y >= self.height_:
            return False
        return True

    def reset(self):
        for col in self.grid_:
            for box in col:
                box.reset()

    def __str__(self):
        return str(self.grid_)
