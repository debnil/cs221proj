import random
import util
from graph import *

def randomAgent(gameState):
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

def humanAgent(gameState):
    while True:
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

class MinimaxAgent:
    def __init__ (self, evaluationFn, depth, player):
        self.evalFn = evaluationFn
        self.depth = depth
        self.player = player # 1 for player 1, -1 for player 2

    def getAction(self, gameState):
        def V_opt(gameState, depth):
            if gameState.isEnd():
                score = gameState.getScore()
                if score > 0:
                    sign = 1
                elif score == 0:
                    sign = 0
                elif score < 0:
                    sign = -1
                return self.player * sign * float("inf"), None
            elif (depth == 0): # Never evaluate with depth = 0 
                return self.evaluationFunction(gameState), None
            elif (gameState.turn == self.player): # Agent's turn
                scoredActions = [(V_opt(gameState.generateSuccessor(move), depth)[0], \
                                 action)  for action in gameState.getValidMoves()]
                #scoredActions = [(V_opt(gameState.generatePacmanSuccessor(action), \
                #                 depth, playerIndex + 1)[0], action) \
                #                 for action in gameState.getLegalPacmanActions()]
                return max(scoredActions)
            else:
                return min((V_opt(gameState.generateSuccessor(move), depth-1)[0], \
                            action) for action in gameState.getValidMoves())
        score, action = V_opt(gameState, self.depth)
        print "Score: %d, Action: %s" % (score, action)
        return action

