import sets

class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.edges = set()

class Edge:
    def __init__(self, x1, y1, x2, y2):
        self.src = Vertex(x1, y1)
        self.dest = Vertex(x2, y2)

    # Returns true if the vertex is one of the endpoints of the edge
    def containsVertex(self, vertex):
        if vertex == self.src or vertex == self.dest:
            return True
        return False
