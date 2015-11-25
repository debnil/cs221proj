import random
import util
import structure
import move
import operator
import pdb
import copy
from move import Move
from transpositionTable import TranspositionTable

class Agent:
    def __init__(self, player):
        self.player_ = player # 1 for player 1, -1 for player 2

    def isWinner(self, value):
        self.winner_ = value

class RandomAgent(Agent):
    def getAction(self, gameState):
        actions = gameState.getValidMoves()
        randomAction = random.choice(tuple(actions))
        return randomAction

class HumanAgent(Agent):
    def getAction(self, gameState):
        while True:
            line = raw_input("Enter (x, y, edge) where (x, y) is the coordinate of a box and edge is (left, right, top, or bottom): ")
            try:
                x, y, edge = (x.strip() for x in line.split(','))
            except TypeError as e:
                print "Somehow we encountered a TypeError", e

            if edge == "left":
                edgeType = structure.Edge.LEFT
            elif edge == "right":
                edgeType = structure.Edge.RIGHT
            elif edge == "top":
                edgeType = structure.Edge.TOP
            elif edge == "bottom":
                edgeType = structure.Edge.BOTTOM
            else:
                print "Not a valid move"
                continue

            action = move.Move(int(x), int(y), edgeType)
            if action in gameState.getValidMoves():
                return action
            else:
                print "Not in the set of valid moves"
                print gameState.getValidMoves()

class MinimaxAgent(Agent):
    def __init__(self, evaluationFn, depth, player, verbose = 0):
        self.evalFn_ = evaluationFn
        self.depth_ = depth
        self.player_ = player # Player 1(1), Player 2(-1)
        self.verbose_ = verbose
        self.cache_ = TranspositionTable() # [Game State, Move] -> Delta score of move
        self.currGameMoves_ = []

    def __printInternalScores(self, score, move, depth, alpha, beta, successor):
        if self.verbose_ >= 3:
            print "Calculated score for agent: ", score, move
            print "Depth: ", depth
            print "Alpha: ", alpha
            print "Beta: ", beta
        if self.verbose_ >= 4:
            util.printGame(successor)

    def __getOrderedValidMoves(self, gameState, depth):
        ''' Returns iterable of valid moves from current game state using alpha-beta
        heuristic for ordering. Only uses chain moves if possible '''
        chainMoves = gameState.getChainMoves() 
        if len(chainMoves) > 0:
            moveSet = chainMoves
        else: # Order the rest of the moves
            moveSet = list(gameState.getValidMoves())
            movesWithoutCapture = gameState.getMovesWithoutCaptures()
            moveSet.sort(key = lambda(move): \
                    random.random() if move in movesWithoutCapture else 0, reverse = True)
                    #move in movesWithoutCapture or \
                    #self.cache_.containsKey((gameState, depth, move)), reverse = True)
        return moveSet

    def getAction(self, gameState):
        def V_opt(gameState, depth, alpha, beta): # Alpha-beta pruning
            if gameState.isEnd():
                return self.evalFn_(self, gameState), None, True
            elif (depth == 0):
                return self.evalFn_(self, gameState), None, True
            elif (gameState.getTurn() == self.player_): # Agent's turn
                V = float("-inf"), None, True
                moveSet = self.__getOrderedValidMoves(gameState, depth)
                currScore = self.evalFn_(self, gameState)
                for move in moveSet:
                    # TODO: Make this score agnostic
                    cacheKey = (gameState, depth, move)
                    successor = gameState.generateSuccessor(move)
                    if self.cache_.containsKey(cacheKey):
                        score = currScore + self.cache_.value(cacheKey)
                        cachable = True # Can cache values that have been cached
                    else:
                        score, _, cachable = V_opt(successor, depth, alpha, beta)
                        if cachable:
                            self.cache_.addKey(cacheKey, score - currScore)
                    V = max(V, (score, move, cachable), key=operator.itemgetter(0))
                    alpha = max(alpha, V[0]) # Update alpha
                    self.__printInternalScores(score, move, depth, alpha, beta, successor)
                    if beta <= alpha: # Prune
                        V = (V[0], V[1], False) # Don't cache if pruned
                        break
                return V
            else: # Opponent's turn
                V = float("inf"), None, True
                moveSet = self.__getOrderedValidMoves(gameState, depth)
                currScore = self.evalFn_(self, gameState)
                for move in moveSet:
                    successor = gameState.generateSuccessor(move)
                    cacheKey = (gameState, depth, move)
                    newDepth = depth - 1
                    if successor.getTurn() != self.player_: # Still opp turn
                        newDepth = depth
                    if self.cache_.containsKey(cacheKey):
                        score = currScore + self.cache_.value(cacheKey)
                        cachable = True # Can cache values that have been cached
                    else:
                        score, _, cachable = V_opt(successor, newDepth, alpha, beta)
                        if cachable:
                            self.cache_.addKey(cacheKey, score - currScore)
                    # Non-cachability should propagate upwards
                    V = min(V, (score, move, cachable), key=operator.itemgetter(0))
                    beta = min(beta, score) # Update beta
                    self.__printInternalScores(score, move, depth, alpha, beta, successor)
                    if beta <= alpha: # Prune
                        V = (V[0], V[1], False)
                        break
                return V

        movesWithoutCaptures = gameState.getMovesWithoutCaptures()
        if len(movesWithoutCaptures) < 4:
            self.calculatedDepth = self.depth_ + 2
        elif len(gameState.getChainMoves()) != 0 and len(gameState.getValidMoves()) < 10:
            self.calculatedDepth = self.depth_ + 1
        else:
            self.calculatedDepth = self.depth_
        if self.verbose_ >= 1:
            print "Searching %d deep" % self.calculatedDepth
        score, action, _ = V_opt(gameState, self.calculatedDepth, float("-inf"), float("inf"))

        self.currGameMoves_.append((gameState, self.calculatedDepth, action))
        print "Score: %f, Action: %s" % (score, action)
        return action
    
    # Update the cache on moves that you lost on
    # Resets internals
    def isWinner(self, value):
        if not value:
            for move in self.currGameMoves_:
                if self.cache_.containsKey(move):
                    self.cache_.updateTable(move, self.cache_.value(move) - 1)
        self.currGameMoves_ = []

def basicEval(agent, gameState):
    return gameState.getScore() * agent.player_ # Positive if player is winning

class TDLearningAgent(MinimaxAgent):
    def __init__(self, depth, player, featureExtractor, verbose = 0):
        MinimaxAgent.__init__(self, TDLearningAgent.TDEval, depth, player, verbose)
        self.weights_ = {}
        self.featureExtractor_ = featureExtractor
        self.NUM_TRIALS_PER_SIMULATION = 10
        self.STEP_SIZE = 0.1
        self.DISCOUNT = 1

    def TDEval(agent, gameState):
        for i in range(agent.NUM_TRIALS_PER_SIMULATION):
            print "%d%% finished simulating." % (i*10)
            agent.__simulate(copy.deepcopy(gameState))

        return agent.getTDScore(agent.featureExtractor_(gameState))
        #return util.dotProduct(agent.weights_, agent.featureExtractor_(gameState))

        return agent.player_ * gameState.getScore()

    def getTDScore(self, features):
        return util.dotProduct(self.weights_, features)

    def __updateWeights(self, currFeatures, nextFeatures, reward):
        # TODO: Fix this
        for feature in currFeatures:
            self.weights_.setdefault(feature, 0)
        for feature in nextFeatures:
            self.weights_.setdefault(feature, 0)
        for feature in currFeatures:
            self.weights_[feature] -= \
                    self.STEP_SIZE*(self.getTDScore(currFeatures) - \
                    (reward + self.DISCOUNT*self.getTDScore(nextFeatures)))\
                    * currFeatures[feature]
    
    # Simulates one game starting from an original game state to completion
    # and updates the weights appropriately
    def __simulate(self, originalState):
        state = originalState
        currFeatures = self.featureExtractor_(state)
        while not state.isEnd():
            move = self.__TDGetAction(state)
            reward = state.getReward(move)
            state = state.generateSuccessor(move)
            nextFeatures = self.featureExtractor_(state)
            self.__updateWeights(currFeatures, nextFeatures, reward)
            currFeatures = nextFeatures

    # Mock up policy for usage in TD Learning
    def __TDGetAction(self, gameState):
        chainMoves = gameState.getChainMoves()
        movesNotLeadingToCapture = gameState.getMovesWithoutCaptures()
        allMoves = gameState.getValidMoves()
        if len(chainMoves) > 0:
            moves = chainMoves
        elif len(movesNotLeadingToCapture) > 0:
            moves = movesNotLeadingToCapture
        else:
            moves = allMoves
        return random.choice(list(moves))

def defaultFeatureExtractor(gameState):
    features = {}
    extractEdgesInBoxesFeature(gameState, features)
    return features

def extractEdgesInBoxesFeature(gameState, features):
    grid = gameState.getGrid()
    for x in range(grid.getWidth()):
        for y in range(grid.getHeight()):
            box = grid.getBox(x, y)
            edgeCount = box.edgeCount()
            features.setdefault("boxes with %d edges" % edgeCount, 0)
            features["boxes with %d edges" % edgeCount] += 1
