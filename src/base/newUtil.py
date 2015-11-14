import structure

def printGame(gameState):
    assert gameState.width > 0
    assert gameState.height > 0
    for y in range(gameState.height): # TODO: Use real fxn
        print "+",
        for x in range(gameState.width):
            currBox = gameState.grid.getBox(x, y)
            if currBox.getEdge(structure.Edge.TOP):
                print "-",
            else:
                print " ",
            print "+",
        print ""
        # Print the left most
        currBox = gameState.grid.getBox(0, y)
        if currBox.getEdge(structure.Edge.LEFT):
            print "|",
        else:
            print " ",
        # Print the middle row
        for x in range(0, gameState.width):
            currBox = gameState.grid.getBox(x, y)
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
    for x in range(gameState.width): # Print the bottom row
        currBox = gameState.grid.getBox(x, y)
        if currBox.getEdge(structure.Edge.TOP):
            print "-",
        else:
            print " ",
        print "+",


