from graph import Vertex

# Prints a DotBoxGame
def printGame(game):
    for y in range(game.height):
        for x in range(game.width): # Print the first line
            currVertex = game.grid[x][y]
            print "+",
            edgeChar = " "
            for edge in currVertex.edges:
                if edge.containsVertex(Vertex(currVertex.x+1, currVertex.y)):
                    edgeChar = "-"
            print edgeChar,
        print ""
        for x in range(game.width):
            currVertex = game.grid[x][y]
            edgeChar = " "
            for edge in currVertex.edges:
                if edge.containsVertex(Vertex(currVertex.x, currVertex.y+1)):
                    edgeChar = "|"
            spacer = " "
            if ((x, y) in game.squares):
                spacer = "1" if game.squares[(x,y)] == 1 else "2"
            print edgeChar, spacer,
        print ""

def boundCheck(x, minBound, maxBound):
    if (x < minBound or x > maxBound):
        return False
    return True
