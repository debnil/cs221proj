import newDotsAndBoxes
import newAgents

agentOne = newAgents.RandomAgent(1)
agentTwo = newAgents.RandomAgent(-1)
game = newDotsAndBoxes.DotBoxGame(4, 3, agentOne, agentTwo, verbose = 3)
firstWins = 0
secondWins = 0
NUM_TRIALS = 1000
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
