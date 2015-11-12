from graph import *
import util
import agents
import copy

class DotBoxGameState:
    def _initializeMoves(self):
        self.moves = []
        for row in range(self.height):
            for col in range(self.width):
                if row+1 < self.height:
                    self.moves.append(Edge(Vertex(col, row), Vertex(col, row+1)))
                if col+1 < self.width:
                    self.moves.append(Edge(Vertex(col, row), Vertex(col+1, row)))

    def __init__(self, game, width, height, score, turn, edges, moves = None):
        self.game = game # For paint purposes
        self.width = width
        self.height = height
        self.score = score
        self.turn = turn
        self.edges = edges
        if moves is None:
            self.moves = []
            self._initializeMoves()
        else:
            self.moves = moves

    def deepCopy(self):
        otherEdges = copy.deepcopy(self.edges)
        otherMoves = copy.deepcopy(self.moves)
        other = DotBoxGameState(self.game, self.width, self.height, self.score, self.turn, \
                                otherEdges, otherMoves)
        return other

    def _restart(self):
        self.score = 0
        self.edges = []
        self._initializeMoves()

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getScore(self):
        return self.score

    def getTurn(self):
        return self.turn

    def getEdges(self):
        return self.edges

    def generateSuccessor(self, edge):
        other = self.deepCopy()
        other.addEdge(edge)
        return other

    # Adds an edge to the state and updates internals
    # Pass game for printing purposes
    def addEdge(self, edge):
        self.edges.append(edge)
        self.moves.remove(edge)

        # Check if you've made a square
        def detectSquare(game, edge):
            edgeSet = game.state.getEdges()
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
                        game.squares[(x, edge.src.y - 1)] = game.state.getTurn()
                if (Edge(Vertex(edge.src.x, edge.src.y), \
                         Vertex(edge.src.x, edge.src.y + 1)) in edgeSet and \
                    Edge(Vertex(edge.dest.x, edge.dest.y), \
                         Vertex(edge.dest.x, edge.dest.y + 1)) in edgeSet and \
                    Edge(Vertex(edge.src.x, edge.src.y + 1), \
                         Vertex(edge.dest.x, edge.dest.y + 1)) in edgeSet):
                        score += 1
                        x = min(edge.src.x, edge.dest.x)
                        game.squares[(x, edge.src.y)] = game.state.getTurn()
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
                        game.squares[(edge.src.x - 1, y)] = game.state.getTurn()
                if (Edge(Vertex(edge.src.x, edge.src.y), \
                         Vertex(edge.src.x + 1, edge.src.y)) in edgeSet and \
                    Edge(Vertex(edge.dest.x, edge.dest.y), \
                         Vertex(edge.dest.x + 1, edge.dest.y)) in edgeSet and \
                    Edge(Vertex(edge.src.x + 1, edge.src.y), \
                         Vertex(edge.dest.x + 1, edge.dest.y)) in edgeSet):
                        score += 1
                        y = min(edge.src.y, edge.dest.y)
                        game.squares[(edge.src.x, y)] = game.state.getTurn()
                return score

        score = detectSquare(self.game, edge)
        self.score += score * self.getTurn()
        if score == 0: # No boxes made
            self.turn *= -1
        return score

    def getValidMoves(self):
        return self.moves

    def isEnd(self):
        return len(self.moves) == 0

    """
    Allows two states to be compared.
    """
    def __eq__( self, other ):
        if other == None: return False
        # TODO Check for type of other
        if not self.width == other.width: return False
        if not self.height == other.height: return False
        if not self.score == other.score: return False
        if not self.turn == other.turn: return False
        if not self.edges == other.edges: return False
        return True

    """
    Allows states to be keys of dictionaries.
    """
    def __hash__( self ):
       return int((hash(self.width) + 29*hash(self.height) + 13*hash(self.score) + 113* hash(self.turn) + 7 * hash(tuple(self.edges))) % 1048575 )

class DotBoxGame:
    # Width and height do NOT specify edges.
    # +-+
    # | | << This is a 1x1 grid
    # +-+
    def __init__(self, width, height, playerOneAgent, playerTwoAgent, verbose = 3):
        self.grid = []
        for x in range(width):
            col = []
            for y in range(height):
                col.append(Vertex(x, y))
            self.grid.append(col)
        self.playerOneAgent = playerOneAgent
        self.playerTwoAgent = playerTwoAgent
        self.state = DotBoxGameState(game = self, \
                                    width = width, \
                                    height = height, \
                                    score = 0, \
                                    turn = 1, \
                                    edges = [])
        self.verbose = verbose
        self.winner = 0
        self.squares = {}

    # Returns the number of boxes made from adding this edge
    # src and dest must be vertices that are in bounds
    def addEdge(self, edge):
        # Make sure that source and dest are in bounds
        src = edge.src
        dest = edge.dest
        if not util.boundCheck(src.x, 0, self.state.getWidth()) or \
           not util.boundCheck(src.y, 0, self.state.getHeight()) or \
           not util.boundCheck(dest.x, 0, self.state.getWidth()) or \
           not util.boundCheck(dest.y, 0, self.state.getHeight()):
           raise ValueError("((%d, %d), (%d, %d)) is not in bounds"  \
                  % (src.x, src.y, dest.x, dest.y))
        self.grid[src.x][src.y].edges.append(edge)
        self.grid[dest.x][dest.y].edges.append(edge)
        self.state = self.state.generateSuccessor(edge)

    def playGame(self):
        # reinitialize all of the internal states
        self.state._restart()
        self.squares = {}
        for y in range(self.state.getHeight()):
            for x in range(self.state.getWidth()):
                game.grid[x][y].edges = []

        while not self.state.isEnd():
            playerNumber = 1 if (self.state.getTurn() == 1) else 2
            if self.verbose >= 3:
                util.printGame(self)
                print "Player %d: " % (playerNumber)
                print "Score: %d" % self.state.getScore()
            if (playerNumber == 1):
                edge = self.playerOneAgent.getAction(self.state)
            else: 
                edge = self.playerTwoAgent.getAction(self.state)
            self.addEdge(edge)
            #numBoxesCompleted = self.addEdge(edge)
            #if (numBoxesCompleted == 0): # Switch turns if no boxes are completed
            #    self.state.turn *= -1
            pause = raw_input()

        if self.state.getScore() < 0:
            self.winner = -1
        else:
            self.winner = 1
        if self.verbose >= 2:
            print "Winner is: ", 1 if self.winner > 0 else 2
            print "Score: %d" % self.state.getScore()
            util.printGame(self)
            
playerOne = agents.RandomAgent(1)
print agents.evalState
playerTwo = agents.MinimaxAgent(agents.evalState, 1, -1)
game = DotBoxGame(3, 4, playerOne, playerTwo, verbose = 3)
game.playGame()
firstWins = 0
for _ in range(1000):
    game.playGame()
    if (game.winner == 1):
        firstWins += 1
print "Win rate is %f" % (float(firstWins) / 1000)
print "First won: %d times" % firstWins
