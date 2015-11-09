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


game = DotBoxGame(5, 3)
