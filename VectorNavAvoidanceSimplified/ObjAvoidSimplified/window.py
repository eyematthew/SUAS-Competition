'''
Created on Jan 10, 2017

@author: phusisian
'''
from ObjAvoidSimplified import *
from time import sleep

class Window:
    CENTERPOINT = (720, 510)

    def __init__(self, drawable, dim):
        self.dim = dim
        self.drawable = drawable
        self.graphWin = GraphWin("Masses", self.dim[0], self.dim[1])
        self.drawLoop()

    def getGraphWin(self):
        return self.graphWin

    def getCenterPoint(self):
        return self.centerPoint

    def drawLoop(self):
        self.drawable.drawStationaryObjects(self)
        while(True):
            self.drawable.avoid_obstacles()
            self.drawable.draw(self)
            sleep(0.01)
