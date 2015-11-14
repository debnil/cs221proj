import random
import util
import structure
import move

class Agent:
    def __init__(self, player):
        self.player = player # 1 for player 1, -1 for player 2

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
            if action in gameState.validMoves:
                return action
            else:
                print "Not in the set of valid moves"
                print gameState.validMoves
