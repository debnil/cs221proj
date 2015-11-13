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
    def __init__ (self, evaluationFn, depth, player, verbose = 0):
        self.evalFn = evaluationFn
        self.depth = depth
        self.player = player #Player 1(1), Player 2(-1)
        self.verbose = verbose

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
                # Only inspect captures if captures exist
                captureMoves = gameState.getCaptureMoves() 
                if len(captureMoves) == 0:
                    moveSet = gameState.getValidMoves()
                else:
                    moveSet = captureMoves

                for move in moveSet:
                    successor = gameState.generateSuccessor(move)
                    score = V_opt(successor, depth, alpha, beta)[0], move
                    if self.verbose >= 3:
                        print "Calculated score for agent: ", score
                        print "Depth: ", depth
                        util.printGame(successor, 8-min(depth, 7))
                    V = max(V, (score[0], move))
                    alpha = max(alpha, V[0]) # Update alpha
                    if beta <= alpha: # Prune
                        break
                return V
            else: # Opponent's turn
                V = float("inf"), None
                # Only inspect captures if captures exist
                captureMoves = gameState.getCaptureMoves()
                if len(captureMoves) == 0:
                    moveSet = gameState.getValidMoves()
                else:
                    moveSet = captureMoves

                for move in moveSet:
                    successor = gameState.generateSuccessor(move)
                    newDepth = depth - 1
                    if successor.getTurn() != self.player: # Still opp turn
                        newDepth = depth
                    score = V_opt(successor, newDepth, alpha, beta)[0], move
                    if self.verbose >= 3:
                        print "Calculated score for opp: ", score
                        print "Depth: ", newDepth
                        util.printGame(successor, 8-min(newDepth, 7))

                    V = min(V, (score[0], move))
                    beta = min(beta, V[0]) # Update beta
                    if beta <= alpha: #Prune
                        break
                return V
            
        if self.depth > 1:
            if len(gameState.getMovesWithoutCapture()) < 5:
                self.depth = 4
        score, action = V_opt(gameState, self.depth, float("-inf"), float("inf"))
        if self.verbose >= 1:
            print "Searching %d deep" % self.depth
        #score, action = V_opt(gameState, 10/len(gameState.moves) + 2, float("-inf"), float("inf"))
        print "Score: %f, Action: %s" % (score, action)
        return action

def evalState(player, gameState):
    #print util.printGame(gameState, True)
    #print "Player: ", player
    #print "evalState: ", gameState.getScore() * player
    return gameState.getScore() * player # Positive if player is winning
