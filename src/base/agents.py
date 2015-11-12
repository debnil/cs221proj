import random
import util
from graph import *

def randomAgent(game):
    while True:
        x1 = random.randint(0, game.width - 1)
        y1 = random.randint(0, game.height - 1)
        delta = random.choice([-1, 1])
        which = random.choice([(0, delta), (delta, 0)])
        x2 = which[0] + x1
        y2 = which[1] + y1
        try:
            edge = Edge(Vertex(x1, y1), Vertex(x2, y2))
            if x2 >= game.width or y2 >= game.height:
                continue
            elif edge in game.edges:
                continue
            elif not util.boundCheck(x1, 0, game.width) or \
                not util.boundCheck(x2, 0, game.width) or \
                not util.boundCheck(y1, 0, game.height) or \
                not util.boundCheck(y2, 0, game.height):
                continue
            else:
                return edge
        except ValueError as e:
            print e

def humanAgent(game):
    while True:
        x1, y1, x2, y2 = (int(x.strip()) for x in raw_input("Enter an edge (x1, y1, x2, y2): ").split(','))
        try:
            edge = Edge(Vertex(x1, y1), Vertex(x2, y2))
            if edge in game.edges:
                print "Edge already in use."
            elif not util.boundCheck(x1, 0, game.width-1) or \
                not util.boundCheck(x2, 0, game.width-1) or \
                not util.boundCheck(y1, 0, game.height-1) or \
                not util.boundCheck(y2, 0, game.height-1):
                print "Edge not in bounds."
            else:
                return edge
        except ValueError as e:
            print e
        

