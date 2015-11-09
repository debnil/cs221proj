from dotBoxesDS import Vertex

# input: grid is a list of lists of vertices
# if I do grid[n], I get the n-1'st column
# if I do grid[n][0], I get the n-1'st by 1
def printGrid(grid):
	numCols = len(grid)
	numRows = len(grid[0])
	for rowIndex in range(numRows):
		currentRow = []
		for colIndex in range(numCols):
			currentRow.append(grid[rowIndex][colIndex])
		for currentVertex in currentRow:
			if currentVertex.edges.containsVertex(Vertex(currentVertex.x, currentVertex.y-1)):
				print "|"
			else:
				print ".",
			if currentVertex.edges.containsVertex(Vertex(currentVertex.x+1, currentVertex.y)):
				print "_",
			else:
				print "	",
		print
	return