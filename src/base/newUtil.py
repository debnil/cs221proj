import structure

def printGame(gameState):
    assert gameState.getWidth() > 0
    assert gameState.getHeight() > 0
    for y in range(gameState.getHeight()): # TODO: Use real fxn
        print "+",
        for x in range(gameState.getWidth()):
            currBox = gameState.getGrid().getBox(x, y)
            if currBox.getEdge(structure.Edge.TOP):
                print "-",
            else:
                print " ",
            print "+",
        print ""
        # Print the left most
        currBox = gameState.getGrid().getBox(0, y)
        if currBox.getEdge(structure.Edge.LEFT):
            print "|",
        else:
            print " ",
        # Print the middle row
        for x in range(0, gameState.getWidth()):
            currBox = gameState.getGrid().getBox(x, y)
            owner = currBox.getOwner()
            if owner == 0:
                print " ",
            else:
                print owner,
            if currBox.getEdge(structure.Edge.RIGHT):
                print "|",
            else:
                print " ",
        print ""
    print "+",
    for x in range(gameState.getWidth()): # Print the bottom row
        currBox = gameState.getGrid().getBox(x, gameState.getHeight() - 1)
        if currBox.getEdge(structure.Edge.BOTTOM):
            print "-",
        else:
            print " ",
        print "+",
    print ""


