from dotBoxesDS import Vertex

# Prints a DotBoxGame
def printGame(game):
    for y in range(game.height):
        for x in range(game.width):
            currVertex = game.grid[x][y]
            vertexChar = "."
            edgeChar = " "
            for edge in currVertex.edges:
                if edge.containsVertex(Vertex(currVertex.x, currVertex.y-1)):
                    vertexChar = "|"
                if edge.containsVertex(Vertex(currVertex.x+1, currVertex.y)):
                    edgeChar = "_"
            print vertexChar,
            print edgeChar,
        print ""
                                    

