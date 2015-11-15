import newDotsAndBoxes
import newAgents
import structure

#agentOne = newAgents.HumanAgent(1)
agentOne = newAgents.MinimaxAgent(evaluationFn = newAgents.basicEval, \
                                  depth = 1, \
                                  player = 1, \
                                  verbose = 2)
agentTwo = newAgents.MinimaxAgent(evaluationFn = newAgents.basicEval, \
                                  depth = 1, \
                                  player = -1, \
                                  verbose = 2)
game = newDotsAndBoxes.DotBoxGame(5, 4, agentOne, agentTwo, verbose = 3)
firstWins = 0
secondWins = 0
NUM_TRIALS = 10
#gridOne = structure.Grid(3, 5)
#gridTwo = structure.Grid(3, 5)
#gridTwo.addEdge(0, 0, structure.Edge.LEFT, 1)
#print hash(gridOne)
#print hash(gridTwo)
for i in range(NUM_TRIALS):
    game.playGame()
    if (i % (NUM_TRIALS/10) == 0):
        print "%d%% finished." % (float(i)/NUM_TRIALS * 100)
    if (game.getWinner() == 1):
        firstWins += 1
    if (game.getWinner() == -1):
        secondWins += 1
print "Win rate is %f%%" % (float(secondWins) / NUM_TRIALS * 100)
print "First won: %d times" % firstWins
print "Second won: %d times" % secondWins
