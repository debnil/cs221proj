from structure import *
from move import *
import copy
import newUtil
import structure

class DotBoxGameState:
    def __init__(self, width, height, score, turn):
        self.width_ = width # Num dots wide
        self.height_ = height # Num dots high
        self.score_ = score
        self.turn_ = turn # -1 for player 2, 1 for player 1
        self.grid_ = Grid(width, height) # Grid of boxes
        self.__createValidMoves()
        
    def generateSuccessor(self, move):
        if move not in self.validMoves_:
            raise ValueError("(%d, %d), %s is not a valid move" % (x, y, edgeType))
        new = copy.deepcopy(self)
        player = 1 if new.getTurn() > 0 else 2
        boxesMade = new.grid_.addEdge(move.x, move.y, move.edgeType, player)
        new.validMoves_.remove(move) 
        new.score_ += boxesMade * new.getTurn()
        if boxesMade == 0:
            new.turn_ *= -1
        return new
    
    def isEnd(self):
        return len(self.validMoves_) == 0

    def reset(self):
        self.score_ = 0
        self.turn_ = 1
        self.grid_.reset()
        self.__createValidMoves()

    ###############################################################
    ########################## ACCESSORS ##########################
    ###############################################################

    def getValidMoves(self):
        return self.validMoves_

    def getScore(self):
        return self.score_

    def getTurn(self):
        return self.turn_

    def getWidth(self):
        return self.width_

    def getHeight(self):
        return self.height_

    def getGrid(self):
        return self.grid_

    ###############################################################
    ######################## PRIVATE FXNS #########################
    ###############################################################

    def __createValidMoves(self):
        self.validMoves_ = set()
        for x in range(self.width_):
            for y in range(self.height_):
                self.validMoves_.add(Move(x, y, structure.Edge.LEFT))
                self.validMoves_.add(Move(x, y, structure.Edge.TOP))

        for x in range(self.width_):
            self.validMoves_.add(Move(x, self.height_ - 1, structure.Edge.BOTTOM))

        for y in range(self.height_):
            self.validMoves_.add(Move(self.width_ - 1, y, structure.Edge.RIGHT))

    def __str__(self):
        return str(self.grid_)

class DotBoxGame:
    # Width and height do NOT specify edges.
    # +-+
    # | | << This is a 1x1 grid
    # +-+
    def __init__(self, width, height, playerOneAgent, playerTwoAgent, verbose = 3):
        self.playerOneAgent_ = playerOneAgent
        self.playerTwoAgent_ = playerTwoAgent
        self.state_ = DotBoxGameState(width = width, \
                                     height = height, \
                                     score = 0, \
                                     turn = 1)
        self.verbose_ = verbose
        self.winner_ = 0

    def playGame(self):
        # reinitialize all of the internal states
        self.state_.reset()

        while not self.state_.isEnd(): #TODO: Use accessors
            playerNumber = 1 if (self.state_.getTurn() == 1) else 2
            if self.verbose_ >= 3:
                newUtil.printGame(self.state_)
                print "Player %d: " % (playerNumber)
                print "Score: %d" % self.state_.getScore()
            if (playerNumber == 1):
                move = self.playerOneAgent_.getAction(self.state_)
            else: 
                move = self.playerTwoAgent_.getAction(self.state_)
            self.state_ = self.state_.generateSuccessor(move)
            #pause = raw_input()

        if self.state_.getScore() < 0:
            self.winner_ = -1
        elif self.state_.getScore() > 0:
            self.winner_ = 1
        else: # Tie
            self.winner_ = 0
        if self.verbose_ >= 2:
            print "Winner is: ", 1 if self.winner_ > 0 else 2
            print "Score: %d" % self.state_.getScore()
            newUtil.printGame(self.state_)

    def getWinner(self):
        return self.winner_

#game = DotBoxGameState(2, 3, 0, 1)
#newGame = game.generateSuccessor(0, 0, structure.Edge.LEFT)
#newUtil.printGame(newGame)
