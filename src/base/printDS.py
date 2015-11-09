from dotBoxesDS import Vertex

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
            print edgeChar, " ",
        print ""

