import sets

class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.edges = set()

class Edge:
    def __init__(self, vertex1, vertex2):
        x1 = vertex1.x
        y1 = vertex1.y
        x2 = vertex2.x
        y2 = vertex2.y
        if not ((abs(x1 - x2) == 1 and abs(y1 - y2) == 0) or \
                (abs(x1 - x2) == 0 and abs(y1 - y2) == 1)): # Must only differ by 1
            raise ValueError("Edge initialized with illegal values.")
        self.src = vertex1
        self.dest = vertex2

    # Returns true if the vertex is one of the endpoints of the edge
    def containsVertex(self, vertex):
        def equalVertex(first, second):
            if first.x == second.x and first.y == second.y:
                return True
            return False

        if equalVertex(self.src, vertex) or equalVertex(self.dest, vertex):
            return True
        return False
