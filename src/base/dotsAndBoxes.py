from structure import *
from move import *
import copy
import util
import structure

###############################################################
############################ STATE ############################
###############################################################

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

    def getCaptureMoves(self):
        captureMoves = set()
        for x in range(self.width_):
            for y in range(self.height_):
                box = self.grid.getBox(x, y)
                if box.edgeCount() == 3:
                    edgeType = box.getMissingEdges()[0]
                    captureMoves.add(Move(x, y, edgeType))
        return captureMoves

    def getChainMoves(self):
        chainMoves = set()
        for x in range(self.width_):
            for y in range(self.height_):
                box = self.grid_.getBox(x, y)
                chain = []
                chainBox = None
                if box.edgeCount() == 3:
                    edgeType = box.getMissingEdges()[0]
                    chain.append(Move(x, y, edgeType))
                    chainX, chainY = structure.getNeighborCoordinates(x, y, edgeType)
                    chainBox = self.grid_.getBox(chainX, chainY)
                    while chainBox is not None and chainBox.edgeCount() == 2: # Half-open chains
                        edges = chainBox.getMissingEdges()
                        if edges[0] == structure.oppositeEdge(edgeType):
                            edgeType = edges[1]
                        else:
                            edgeType = edges[0]
                        chain.append(Move(chainX, chainY, edgeType))
                        chainX, chainY = \
                                structure.getNeighborCoordinates(chainX, chainY, edgeType)
                        chainBox = self.grid_.getBox(chainX, chainY)
                if chainBox is not None and chainBox.edgeCount() == 3: # Closed chain
                    if len(chain) > 0:
                        chainMoves.add(chain[0])
                        if len(chain) == 3: # 4 hard-hearted handout
                            chainMoves.add(chain[1])
                else: # Half-open chain
                    if len(chain) == 1 or len(chain) >= 3:
                        chainMoves.add(chain[0])
                    elif len(chain) == 2: # Hard-hearted handout
                        chainMoves.add(chain[0])
                        chainMoves.add(chain[-1])
        return chainMoves

    # Returns the set of moves that will not result in a possible capture
    def getMovesWithoutCaptures(self):
        moves = set()
        for x in range(self.width_):
            for y in range(self.height_):
                box = self.grid_.getBox(x, y)
                if box.edgeCount() <= 1:
                    edges = box.getMissingEdges()
                    for edge in edges:
                        neighborX, neighborY = \
                                structure.getNeighborCoordinates(x, y, edge)
                        neighbor = self.grid_.getBox(neighborX, neighborY)
                        if neighbor is None or neighbor.edgeCount() <= 1:
                            moves.add(Move(x, y, edge))
        return moves

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

    def __hash__(self):
        return hash((self.grid_, self.turn_, self.score_))

    def __eq__(self, other):
        if other is None and self is not None:
            return False
        if self is None and other is not None:
            return False
        if self is None and other is None:
            return True
        if self.width_ != other.width_:
            return False
        if self.height_ != other.height_:
            return False
        if self.turn_ != other.turn_:
            return False
        if self.grid_ != other.grid_:
            return False
        return True

    def __ne__(self, other):
        return not self == other

###############################################################
############################# GAME ############################
###############################################################

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

    def playGame(self, fileName = None, load = False):
        # Reinitialize all of the internal states
        self.state_.reset()
        if load:
            self.loadStateFromFile(fileName)

        while not self.state_.isEnd(): 
            playerNumber = 1 if (self.state_.getTurn() == 1) else 2
            if self.verbose_ >= 3:
                util.printGame(self.state_)
                print "Player %d: " % (playerNumber)
                print "Score: %d" % self.state_.getScore()
            if (playerNumber == 1):
                move = self.playerOneAgent_.getAction(self.state_)
            else: 
                move = self.playerTwoAgent_.getAction(self.state_)
            self.state_ = self.state_.generateSuccessor(move)

        if self.state_.getScore() < 0:
            self.winner_ = -1
            self.playerOneAgent_.isWinner(False)
            self.playerTwoAgent_.isWinner(True)
        elif self.state_.getScore() > 0:
            self.winner_ = 1
            self.playerOneAgent_.isWinner(True)
            self.playerTwoAgent_.isWinner(False)
        else: # Tie
            self.winner_ = 0
        if self.verbose_ >= 2:
            print "Winner is: ", 1 if self.winner_ > 0 else 2
            print "Score: %d" % self.state_.getScore()
            util.printGame(self.state_)

    def getWinner(self):
        return self.winner_

    def loadStateFromFile(self, fileName):
        stateFile = open(fileName, 'r')
        for line in stateFile:
            if line[0] == '#': # Skip comments
                continue
            move = Move.stringToMove(line)
            self.state_ = self.state_.generateSuccessor(move)
