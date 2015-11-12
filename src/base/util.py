from graph import Vertex

# Prints a DotBoxGame
def printGame(gameState, tab = False):
    for y in range(gameState.getHeight()):
        if tab:
            print "\t\t",
        for x in range(gameState.getWidth()): # Print the first line
            currVertex = gameState.grid[x][y]
            print "+",
            edgeChar = " "
            for edge in currVertex.edges:
                if edge.containsVertex(Vertex(currVertex.x+1, currVertex.y)):
                    edgeChar = "-"
            print edgeChar,
        print ""
        if tab:
            print "\t\t",
        for x in range(gameState.getWidth()):
            currVertex = gameState.grid[x][y]
            edgeChar = " "
            for edge in currVertex.edges:
                if edge.containsVertex(Vertex(currVertex.x, currVertex.y+1)):
                    edgeChar = "|"
            spacer = " "
            if ((x, y) in gameState.squares):
                spacer = "1" if gameState.squares[(x,y)] == 1 else "2"
            print edgeChar, spacer,
        print ""

def boundCheck(x, minBound, maxBound):
    if (x < minBound or x > maxBound):
        return False
    return True
