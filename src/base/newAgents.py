import random
import util

class Agent:
    def __init__(self, player):
        self.player = player # 1 for player 1, -1 for player 2

class RandomAgent(Agent):
    def getAction(self, gameState):
        actions = gameState.getValidMoves()
        randomAction = random.choice(tuple(actions))
        return randomAction
