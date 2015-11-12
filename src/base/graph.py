import sets

class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.edges = []

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self == other

class Edge:
    def __init__(self, vertex1, vertex2):
        x1 = vertex1.x
        y1 = vertex1.y
        x2 = vertex2.x
        y2 = vertex2.y
        if not ((abs(x1 - x2) == 1 and abs(y1 - y2) == 0) or \
                (abs(x1 - x2) == 0 and abs(y1 - y2) == 1)): # Must only differ by 1
            raise ValueError("Edge initialized with illegal values. (%d, %d, %d, %d)" \
                             % (x1, y1, x2, y2))
        self.src = vertex1
        self.dest = vertex2

    # Returns true if the vertex is one of the endpoints of the edge
    def containsVertex(self, vertex):
        if self.src == vertex or self.dest == vertex:
            return True
        else:
            return False

    def __eq__(self, other):
        if self.src == other.src and self.dest == other.dest:
            return True
        elif self.dest == other.src and self.src == other.dest:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "((%d, %d) <-> (%d, %d))" % (self.src.x, self.src.y, self.dest.x, self.dest.y)

    def __repr__(self):
        return self.__str__()
