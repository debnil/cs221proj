from dotBoxesDS import *

class DotBoxGame:
    # Width and height do NOT specify edges.
    # ._. 
    # |_| << This is a 1x1 grid
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = []
        for r in range(height):
            row = []
            for c in range(width):
                row.append(Vertex(c, r))
            self.grid.append(row)
        self.edges = set()

    # src and dest must be vertices that are in bounds
    def addEdge(self, src, dest):
        def boundCheck(x, minBound, maxBound):
            if (x < minBound or x > maxBound):
                raise ValueException("%d is out of bounds" % x)

game = DotBoxGame(5, 3)
