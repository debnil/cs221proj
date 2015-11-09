import random
import printDS
from dotBoxesDS import *

def randomAgent(game):
    while True:
        x1 = random.randint(0, game.width - 1)
        y1 = random.randint(0, game.height - 1)
        delta = random.choice([-1, 1])
        which = random.choice([(0, delta), (delta, 0)])
        x2 = which[0] + x1
        y2 = which[1] + y1
        try:
            edge = Edge(Vertex(x1, y1), Vertex(x2, y2))
            if x2 >= game.width or y2 >= game.height:
                continue
            elif edge in game.edges:
                continue
            elif not boundCheck(x1, 0, game.width) or \
                not boundCheck(x2, 0, game.width) or \
                not boundCheck(y1, 0, game.height) or \
                not boundCheck(y2, 0, game.height):
                continue
            else:
                return edge
        except ValueError as e:
            print e

def humanPlayer(game):
    while True:
        x1, y1, x2, y2 = (int(x.strip()) for x in raw_input("Enter an edge (x1, y1, x2, y2): ").split(','))
        try:
            edge = Edge(Vertex(x1, y1), Vertex(x2, y2))
            if edge in game.edges:
                print "Edge already in use."
            elif not boundCheck(x1, 0, game.width-1) or \
                not boundCheck(x2, 0, game.width-1) or \
                not boundCheck(y1, 0, game.height-1) or \
                not boundCheck(y2, 0, game.height-1):
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
        for x in range(width):
            col = []
            for y in range(height):
                col.append(Vertex(x, y))
            self.grid.append(col)
        self.edges = []
        self.playerOneFn = playerOneFn
        self.playerTwoFn = playerTwoFn
        self.score = 0
        self.turn = 1 # PlayerOne starts
        self.verbose = verbose
        self.winner = 0
        self.squares = {}

    # Returns the number of boxes made from adding this edge
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
        self.grid[src.x][src.y].edges.append(edge)
        self.grid[dest.x][dest.y].edges.append(edge)
        self.edges.append(edge)

        # Check if you've made a square
        def detectSquare(game, edge):
            edgeSet = game.edges
            if (abs(edge.src.x - edge.dest.x) == 1): # Horizontal
                score = 0
                if (Edge(Vertex(edge.src.x, edge.src.y), \
                         Vertex(edge.src.x, edge.src.y - 1)) in edgeSet and \
                    Edge(Vertex(edge.dest.x, edge.dest.y), \
                         Vertex(edge.dest.x, edge.dest.y - 1)) in edgeSet and \
                    Edge(Vertex(edge.src.x, edge.src.y - 1), \
                         Vertex(edge.dest.x, edge.dest.y - 1)) in edgeSet):
                        score += 1
                        x = min(edge.src.x, edge.dest.x)
                        game.squares[(x, edge.src.y - 1)] = game.turn
                if (Edge(Vertex(edge.src.x, edge.src.y), \
                         Vertex(edge.src.x, edge.src.y + 1)) in edgeSet and \
                    Edge(Vertex(edge.dest.x, edge.dest.y), \
                         Vertex(edge.dest.x, edge.dest.y + 1)) in edgeSet and \
                    Edge(Vertex(edge.src.x, edge.src.y + 1), \
                         Vertex(edge.dest.x, edge.dest.y + 1)) in edgeSet):
                        score += 1
                        x = min(edge.src.x, edge.dest.x)
                        game.squares[(x, edge.src.y)] = game.turn
                return score
            else: #Vertical line
                score = 0
                if (Edge(Vertex(edge.src.x, edge.src.y), \
                         Vertex(edge.src.x - 1, edge.src.y)) in edgeSet and \
                    Edge(Vertex(edge.dest.x, edge.dest.y), \
                         Vertex(edge.dest.x - 1, edge.dest.y)) in edgeSet and \
                    Edge(Vertex(edge.src.x - 1, edge.src.y), \
                         Vertex(edge.dest.x - 1, edge.dest.y)) in edgeSet):
                        score += 1
                        y = min(edge.src.y, edge.dest.y)
                        game.squares[(edge.src.x - 1, y)] = game.turn
                if (Edge(Vertex(edge.src.x, edge.src.y), \
                         Vertex(edge.src.x + 1, edge.src.y)) in edgeSet and \
                    Edge(Vertex(edge.dest.x, edge.dest.y), \
                         Vertex(edge.dest.x + 1, edge.dest.y)) in edgeSet and \
                    Edge(Vertex(edge.src.x + 1, edge.src.y), \
                         Vertex(edge.dest.x + 1, edge.dest.y)) in edgeSet):
                        score += 1
                        y = min(edge.src.y, edge.dest.y)
                        game.squares[(edge.src.x, y)] = game.turn
                return score

        score = detectSquare(self, edge)
        if self.verbose >= 3:
            print "Score changed by: %d" % score
        self.score += score * self.turn
        return score

    def playGame(self):
        self.score = 0
        self.edges = []
        while len(self.edges) != (self.width - 1) * self.height + \
                (self.height - 1) * self.width:
            playerNumber = 1 if (self.turn == 1) else 2
            if self.verbose >= 3:
                printDS.printGame(self)
                print "Player %d: " % (playerNumber)
                print "Score: %d" % self.score
            if (playerNumber == 1):
                edge = self.playerOneFn(self)
            else: 
                edge = self.playerTwoFn(self)
            numBoxesCompleted = self.addEdge(edge)
            if (numBoxesCompleted == 0): # Switch turns if no boxes are completed
                self.turn *= -1
            pause = raw_input()
        if self.score < 0:
            self.winner = -1
        else:
            self.winner = 1
        if self.verbose >= 2:
            print "Winner is: ", 1 if self.winner > 0 else 2
            print "Score: %d" % self.score
            printDS.printGame(self)
            
game = DotBoxGame(3, 3, randomAgent, randomAgent, verbose = 3)
game.playGame()
firstWins = 0
#for _ in range(1000):
#    game.playGame()
#    if (game.winner == 1):
#        firstWins += 1
#print "Win rate is %f" % (float(firstWins) / 1000)
#print "First won: %d times" % firstWins

#game.addEdge(Edge(Vertex(0, 0), Vertex(1, 0)))
#print ""
#printDS.printGrid(game)
#game.addEdge(Edge(Vertex(4, 0), Vertex(4, 1)))
#print ""
#printDS.printGrid(game)
#pl
