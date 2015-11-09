import printDS
from dotBoxesDS import *

def humanPlayer(game):
    while True:
        x1, y1, x2, y2 = (int(x.strip()) for x in raw_input("Enter an edge (x1, y1, x2, y2): ").split(','))
        try:
            edge = Edge(Vertex(x1, y1), Vertex(x2, y2))
            if edge in game.edges:
                print "Edge already in use."
            elif not boundCheck(x1, 0, game.width) or \
                not boundCheck(x2, 0, game.width) or \
                not boundCheck(y1, 0, game.height) or \
                not boundCheck(y2, 0, game.height):
                print "Edge not in bounds."
            else:
                return edge
        except ValueError as e:
            print e
        
def boundCheck(x, minBound, maxBound):
    if (x < minBound or x > maxBound):
        return False
    return True

class DotBoxGame:
    # Width and height do NOT specify edges.
    # ._. 
    # |_| << This is a 1x1 grid
    def __init__(self, width, height, playerOneFn = humanPlayer, playerTwoFn = humanPlayer, verbose = 3):
        self.width = width
        self.height = height
        self.grid = []
        #for r in range(height):
        #    row = []
        #    for c in range(width):
        #        row.append(Vertex(c, r))
        #    self.grid.append(row)
        for x in range(width):
            col = []
            for y in range(height):
                col.append(Vertex(x, y))
            self.grid.append(col)
        self.edges = set()
        self.playerOneFn = playerOneFn
        self.playerTwoFn = playerTwoFn
        self.score = 0
        self.turn = 1 # PlayerOne starts
        self.verbose = verbose

    # src and dest must be vertices that are in bounds
    def addEdge(self, edge):
        # Make sure that source and dest are in bounds
        src = edge.src
        dest = edge.dest
        if not boundCheck(src.x, 0, self.width) or \
           not boundCheck(src.y, 0, self.height) or \
           not boundCheck(dest.x, 0, self.width) or \
           not boundCheck(dest.y, 0, self.height):
           raise ValueError("((%d, %d), (%d, %d)) is not in bounds"  \
                   % (src.x, src.y, dest.x, dest.y))
        self.grid[src.x][src.y].edges.add(edge)
        self.grid[dest.x][dest.y].edges.add(edge)
        self.edges.add(edge)

    def playGame(self):
        while len(self.edges) != (self.width - 1) * self.height + \
                (self.height - 1) * self.width:
            if self.verbose >= 3:
                print "Player One: "
                print "Score: %d" % self.score
                printDS.printGame(self)
            edge = self.playerOneFn(self)
            self.addEdge(edge)
            if self.verbose >= 3:
                print "Player Two: "
                print "Score: %d" % self.score
                printDS.printGame(self)
            edge = self.playerTwoFn(self)
            self.addEdge(edge)

game = DotBoxGame(5, 3)
game.playGame()
#printDS.printGrid(game)
#game.addEdge(Edge(Vertex(0, 0), Vertex(1, 0)))
#print ""
#printDS.printGrid(game)
#game.addEdge(Edge(Vertex(4, 0), Vertex(4, 1)))
#print ""
#printDS.printGrid(game)
#pl
