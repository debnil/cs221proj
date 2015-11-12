import random
import util
from graph import *

class Agent:
    def __init__(self, player):
        self.player = player # 1 for player 1, -1 for player 2

class RandomAgent(Agent):
    def getAction(self, gameState):
        while True:
            x1 = random.randint(0, gameState.width - 1)
            y1 = random.randint(0, gameState.height - 1)
            delta = random.choice([-1, 1])
            which = random.choice([(0, delta), (delta, 0)])
            x2 = which[0] + x1
            y2 = which[1] + y1
            try:
                edge = Edge(Vertex(x1, y1), Vertex(x2, y2))
                if x2 >= gameState.width or y2 >= gameState.height:
                    continue
                elif edge in gameState.edges:
                    continue
                elif not util.boundCheck(x1, 0, gameState.width) or \
                    not util.boundCheck(x2, 0, gameState.width) or \
                    not util.boundCheck(y1, 0, gameState.height) or \
                    not util.boundCheck(y2, 0, gameState.height):
                    continue
                else:
                    return edge
            except ValueError as e:
                print e

class HumanAgent(Agent):
    def getAction(self, gameState):
        while True:
            #TODO: Error handling and input sanitizing
            x1, y1, x2, y2 = (int(x.strip()) for x in raw_input("Enter an edge (x1, y1, x2, y2): ").split(','))
            try:
                edge = Edge(Vertex(x1, y1), Vertex(x2, y2))
                if edge in gameState.edges:
                    print "Edge already in use."
                elif not util.boundCheck(x1, 0, gameState.width-1) or \
                    not util.boundCheck(x2, 0, gameState.width-1) or \
                    not util.boundCheck(y1, 0, gameState.height-1) or \
                    not util.boundCheck(y2, 0, gameState.height-1):
                    print "Edge not in bounds."
                else:
                    return edge
            except ValueError as e:
                print e

class MinimaxAgent(Agent):
    def __init__ (self, evaluationFn, depth, player):
        self.evalFn = evaluationFn
        self.depth = depth
        self.player = player #Player 1(1), Player 2(-1)

    def getAction(self, gameState):
        def V_opt(gameState, depth, alpha, beta): # Alpha-beta pruning
            if gameState.isEnd():
                #print gameState
                #print "I'm in an end state! :)"
                score = gameState.getScore()
                if score * self.player > 0:
                    return float("inf"), None
                elif score == 0:
                    return 0, None
                else:
                    return float("-inf"), None
            elif (depth == 0):
                return self.evalFn(self.player, gameState), None
            elif (gameState.turn == self.player): # Agent's turn
                V = float("-inf"), None
                for move in gameState.getValidMoves():
                    successor = gameState.generateSuccessor(move)
                    V = max(V, (V_opt(successor, depth, alpha, beta)[0], move))
                    alpha = max(alpha, V[0]) # Update alpha
                    if beta <= alpha: # Prune
                        break
                return V
            else: # Opponent's turn
                V = float("inf"), None
                for move in gameState.getValidMoves():
                    successor = gameState.generateSuccessor(move)
                    V = min(V, (V_opt(successor, depth - 1, alpha, beta)[0], move))
                    beta = min(beta, V[0]) # Update beta
                    if beta <= alpha: #Prune
                        break
                return V
        #def V_opt(gameState, depth):
        #    if gameState.isEnd():
        #        #print gameState
        #        #print "I'm in an end state! :)"
        #        score = gameState.getScore()
        #        if score * self.player > 0:
        #            return float("inf"), None
        #        elif score == 0:
        #            return 0, None
        #        else:
        #            return float("-inf"), None
        #    elif (depth == 0): # Never evaluate with depth = 0 
        #        return self.evalFn(self.player, gameState), None
        #    elif (gameState.turn == self.player): # Agent's turn
        #        scoredActions = [(V_opt(gameState.generateSuccessor(move), \
        #                        depth)[0], move) for move in gameState.getValidMoves()]
        #        bestAction = max(scoredActions)
        #        #print bestAction[1]
        #        return bestAction
        #    else:
        #        #scoredActions = [(V_opt(gameState.generateSuccessor(move), \
        #        #                  depth-1)[0], move, gameState.generateSuccessor(move)) for move in gameState.getValidMoves()] 
        #        bestAction = min((V_opt(gameState.generateSuccessor(move), \
        #                    depth-1)[0], move) for move in gameState.getValidMoves())
        #        #print bestAction
        #        #print "BEGIN"
        #        #for score, move, state in scoredActions:
        #        #    print "Score: ", score
        #        #    util.printGame(state)
        #        #print "END"
        #        return bestAction

        #score, action = V_opt(gameState, self.depth)
        print "Searching %d deep" % (10/len(gameState.moves) + 2)
        score, action = V_opt(gameState, 8/len(gameState.moves) + 1, float("-inf"), float("inf"))
        #print "Score: %f, Action: %s" % (score, action)
        return action

def evalState(player, gameState):
    #print util.printGame(gameState, True)
    #print "Score: ", gameState.getScore() * player
    return gameState.getScore() * player # Positive if player is winning
