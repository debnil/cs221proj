import random
import newUtil
import structure
import move

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
        self.cache_ = {} # Map from state to delta score
        self.thisGameCache_ = []

    def getAction(self, gameState):
        def V_opt(gameState, depth, alpha, beta): # Alpha-beta pruning
            if gameState.isEnd():
                return self.evalFn_(self.player_, gameState), None
                #score = gameState.getScore()
                #if score * self.player_ > 0:
                #    return float("inf"), None
                #elif score == 0:
                #    return 0, None
                #else:
                #    return float("-inf"), None
            elif (depth == 0):
                return self.evalFn_(self.player_, gameState), None
            elif (gameState.getTurn() == self.player_): # Agent's turn
                #stateKey = (tuple(gameState.grid_), depth)
                #if stateKey in self.cache_:
                #    return self.cache_[stateKey][0] + gameState.getScore(), self.cache_[stateKey][1]
                hashedState = hash((gameState, depth, gameState.getScore()))
                if hashedState in self.cache_ and depth != self.depth_:
                    #print "Retrieving cached value"
                    return self.cache_[hashedState]
                V = float("-inf"), None
                chainMoves = gameState.getChainMoves() 
                if len(chainMoves) > 0:
                    moveSet = chainMoves
                else:
                    moveSet = gameState.getValidMoves()

                if calculatedDepth == depth and len(moveSet) == 1:
                    return 0, moveSet.pop()

                for move in sorted(moveSet):
                    successor = gameState.generateSuccessor(move)
                    score = V_opt(successor, depth, alpha, beta)[0], move
                    V = max(V, (score[0], move))
                    alpha = max(alpha, V[0]) # Update alpha
                    if self.verbose_ >= 3:
                        print "Calculated score for agent: ", score
                        print "Depth: ", depth
                        print "Alpha: ", alpha
                        print "Beta: ", beta
                    if self.verbose_ >= 4:
                        newUtil.printGame(successor)
                    if beta <= alpha: # Prune
                        break
                #self.cache_[stateKey] = (V[0] - gameState.getScore(), V[1])
                #self.cache_[hashedState] = (V[0] - gameState.getScore(), V[1])
                self.cache_[hashedState] = V
                if depth == self.depth_:
                    self.thisGameCache_.append(hashedState)
                return V
            else: # Opponent's turn
                V = float("inf"), None

                chainMoves = gameState.getChainMoves() 
                if len(chainMoves) > 0:
                    moveSet = chainMoves
                else:
                    moveSet = gameState.getValidMoves()

                for move in sorted(moveSet):
                    successor = gameState.generateSuccessor(move)
                    newDepth = depth - 1
                    if successor.getTurn() != self.player_: # Still opp turn
                        newDepth = depth
                    score = V_opt(successor, newDepth, alpha, beta)[0], move
                    V = min(V, (score[0], move))
                    beta = min(beta, V[0]) # Update beta
                    if self.verbose_ >= 3:
                        print "Calculated score for opp: ", score
                        print "Depth: ", depth
                        print "Alpha: ", alpha
                        print "Beta: ", beta
                    if self.verbose_ >= 4:
                        newUtil.printGame(successor)

                    if beta <= alpha: #Prune
                        V = (float("-inf"), V[1])
                        break
                return V

        movesWithoutCaptures = gameState.getMovesWithoutCaptures()
        #print "Moves without causing captures: ", movesWithoutCaptures
        #print "Moves without causing captures: ", len(movesWithoutCaptures)
        if len(movesWithoutCaptures) < 4:
            calculatedDepth = self.depth_ + 1
        elif len(gameState.getChainMoves()) != 0 and len(gameState.getValidMoves()) < 10:
            calculatedDepth = self.depth_ + 1
        else:
            calculatedDepth = self.depth_
        if self.verbose_ >= 1:
            print "Searching %d deep" % self.depth_
        score, action = V_opt(gameState, calculatedDepth, float("-inf"), float("inf"))
        print "Score: %f, Action: %s" % (score, action)
        return action

    def isWinner(self, value):
        # Update the cache on moves that you lost on
        if not value:
            for move in self.thisGameCache_:
                self.cache_[move] = (self.cache_[move][0] - 1, self.cache_[move][1])

def basicEval(player, gameState):
    return gameState.getScore() * player # Positive if player is winning

