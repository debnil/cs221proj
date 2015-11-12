from graph import *
import util
import agents

class DotBoxGame:
    # Width and height do NOT specify edges.
    # +-+
    # | | << This is a 1x1 grid
    # +-+
    def __init__(self, width, height, playerOneFn = agents.humanAgent, playerTwoFn = agents.humanAgent, verbose = 3):
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
        if not util.boundCheck(src.x, 0, self.width) or \
           not util.boundCheck(src.y, 0, self.height) or \
           not util.boundCheck(dest.x, 0, self.width) or \
           not util.boundCheck(dest.y, 0, self.height):
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
        # reinitialize all of the internal states
        self.score = 0
        self.edges = []
        self.squares = {}
        for y in range(game.height):
            for x in range(game.width):
                game.grid[x][y].edges = []

        while len(self.edges) != (self.width - 1) * self.height + \
                (self.height - 1) * self.width:
            playerNumber = 1 if (self.turn == 1) else 2
            if self.verbose >= 3:
                util.printGame(self)
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
            util.printGame(self)
            
game = DotBoxGame(3, 3, agents.randomAgent, agents.randomAgent, verbose = 3)
game.playGame()
firstWins = 0
for _ in range(1000):
    game.playGame()
    if (game.winner == 1):
        firstWins += 1
print "Win rate is %f" % (float(firstWins) / 1000)
print "First won: %d times" % firstWins
