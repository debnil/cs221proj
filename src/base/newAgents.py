import random
import newUtil
import structure
import move

class Agent:
    def __init__(self, player):
        self.player_ = player # 1 for player 1, -1 for player 2

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

    def getAction(self, gameState):
        def V_opt(gameState, depth, alpha, beta): # Alpha-beta pruning
            if gameState.isEnd():
                score = gameState.getScore()
                if score * self.player_ > 0:
                    return float("inf"), None
                elif score == 0:
                    return 0, None
                else:
                    return float("-inf"), None
            elif (depth == 0):
                return self.evalFn_(self.player_, gameState), None
            elif (gameState.getTurn() == self.player_): # Agent's turn
                V = float("-inf"), None
                chainMoves = gameState.getChainMoves() 
                if len(chainMoves) > 0:
                    moveSet = chainMoves
                else:
                    moveSet = gameState.getValidMoves()

                for move in moveSet:
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
                return V
            else: # Opponent's turn
                V = float("inf"), None

                chainMoves = gameState.getChainMoves() 
                if len(chainMoves) > 0:
                    moveSet = chainMoves
                else:
                    moveSet = gameState.getValidMoves()

                for move in moveSet:
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

        if raw_input("Do you want to make a move? [Y/n]") == "Y":
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

        if len(gameState.getChainMoves()) != 0:
            self.depth_ = 4
        else:
            self.depth_ = 2
        score, action = V_opt(gameState, self.depth_, float("-inf"), float("inf"))
        if self.verbose_ >= 1:
            print "Searching %d deep" % self.depth_
        print "Score: %f, Action: %s" % (score, action)
        return action

def basicEval(player, gameState):
    return gameState.getScore() * player # Positive if player is winning

