import dotsAndBoxes
import agents
import structure
import sys

#agentOne = agents.HumanAgent(1)
agentOne = agents.MinimaxAgent(evaluationFn = agents.basicEval, \
                                  depth = 3, \
                                  player = 1, \
                                  verbose = 2)
'''agentTwo = agents.MinimaxAgent(evaluationFn = agents.basicEval, \
                                  depth = 3, \
                                  player = -1, \
                                  verbose = 2)'''
agentTwo = agents.HumanAgent(1)
game = dotsAndBoxes.DotBoxGame(3, 3, agentOne, agentTwo, verbose = 3)
if len(sys.argv) > 1:
    load = True
    fileName = sys.argv[1]
else:
    load = False
    fileName = None
firstWins = 0
secondWins = 0
NUM_TRIALS = 10
for i in range(NUM_TRIALS):
    game.playGame(fileName, load)
    if (i % (NUM_TRIALS/10) == 0):
        print "%d%% finished." % (float(i)/NUM_TRIALS * 100)
    if (game.getWinner() == 1):
        firstWins += 1
    if (game.getWinner() == -1):
        secondWins += 1
print "Win rate is %f%%" % (float(secondWins) / NUM_TRIALS * 100)
print "First won: %d times" % firstWins
print "Second won: %d times" % secondWins
