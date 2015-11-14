from structure import *
from move import *
import copy
import newUtil
import structure
import newAgents

class DotBoxGameState:
    def __init__(self, width, height, score, turn):
        self.width = width # Num dots wide
        self.height = height # Num dots high
        self.score = score
        self.turn = turn # -1 for player 2, 1 for player 1
        self.grid = Grid(width, height) # Grid of boxes
        self.__createValidMoves()
        
    def generateSuccessor(self, move):
        if move not in self.validMoves:
            raise ValueError("(%d, %d), %s is not a valid move" % (x, y, edgeType))
        new = copy.deepcopy(self)
        player = 1 if new.turn > 0 else 2
        boxesMade = new.grid.addEdge(move.x, move.y, move.edgeType, player)
        new.validMoves.remove(move) 
        new.score += boxesMade * new.turn
        if boxesMade == 0:
            new.turn *= -1
        print new
        return new
    
    def getValidMoves(self):
        return self.validMoves

    def isEnd(self):
        return len(self.validMoves) == 0

    def reset(self):
        self.score = 0
        self.turn = 1
        self.grid.reset()
        self.__createValidMoves()

    def __createValidMoves(self):
        self.validMoves = set()
        for x in range(self.width):
            for y in range(self.height):
                self.validMoves.add(Move(x, y, structure.Edge.LEFT))
                self.validMoves.add(Move(x, y, structure.Edge.TOP))

        for x in range(self.width):
            self.validMoves.add(Move(x, self.height - 1, structure.Edge.BOTTOM))

        for y in range(self.height):
            self.validMoves.add(Move(self.width - 1, y, structure.Edge.RIGHT))

    ###############################################################
    ########################## ACCESSORS ##########################
    ###############################################################

    #TODO: Fill this out

class DotBoxGame:
    # Width and height do NOT specify edges.
    # +-+
    # | | << This is a 1x1 grid
    # +-+
    def __init__(self, width, height, playerOneAgent, playerTwoAgent, verbose = 3):
        self.playerOneAgent = playerOneAgent
        self.playerTwoAgent = playerTwoAgent
        self.state = DotBoxGameState(width = width, \
                                     height = height, \
                                     score = 0, \
                                     turn = 1)
        self.verbose = verbose
        self.winner = 0

    def playGame(self):
        # reinitialize all of the internal states
        self.state.reset()

        while not self.state.isEnd(): #TODO: Use accessors
            playerNumber = 1 if (self.state.turn == 1) else 2
            if self.verbose >= 3:
                newUtil.printGame(self.state)
                print "Player %d: " % (playerNumber)
                print "Score: %d" % self.state.score
            if (playerNumber == 1):
                move = self.playerOneAgent.getAction(self.state)
            else: 
                move = self.playerTwoAgent.getAction(self.state)
            self.state = self.state.generateSuccessor(move)
            #pause = raw_input()

        if self.state.score < 0:
            self.winner = -1
        elif self.state.score > 0:
            self.winner = 1
        else: # Tie
            self.winner = 0
        if self.verbose >= 2:
            print "Winner is: ", 1 if self.winner > 0 else 2
            print "Score: %d" % self.state.score
            newUtil.printGame(self.state)

#game = DotBoxGameState(2, 3, 0, 1)
#newGame = game.generateSuccessor(0, 0, structure.Edge.LEFT)
#newUtil.printGame(newGame)

agentOne = newAgents.RandomAgent(1)
agentTwo = newAgents.HumanAgent(-1)
game = DotBoxGame(4, 3, agentOne, agentTwo, verbose = 3)
firstWins = 0
secondWins = 0
NUM_TRIALS = 1000
for i in range(NUM_TRIALS):
    game.playGame()
    if (i % (NUM_TRIALS/10) == 0):
        print "%d%% finished." % (float(i)/NUM_TRIALS * 100)
    if (game.winner == 1):
        firstWins += 1
    if (game.winner == -1):
        secondWins += 1
print "Win rate is %f%%" % (float(secondWins) / NUM_TRIALS * 100)
print "First won: %d times" % firstWins
print "Second won: %d times" % secondWins
