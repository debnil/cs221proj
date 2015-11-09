import sets

class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.edges = set()

class Edge:
    def __init__(self, x1, y1, x2, y2):
        self.src = (x1, y1)
        self.dest = (x2, y2)
