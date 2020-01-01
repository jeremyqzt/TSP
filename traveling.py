import matplotlib.pyplot as plt
import numpy as np
import time
import random
import itertools
import math
import os
import threading

class plotCompareProblem():
    #So we don't use the edges of the graph
    pltMin = 2
    pltMax = 29

    def __init__(self, count=5, start=(0,0)):
        # 0, 0 is the start
        self.pltCount = count
        self.start = start
        self.xdata = [start[0]]
        self.ydata = [start[1]]
        self.id = 1
        self.plt = plt
        self.plt.ion()
        self.figure, (self.ax, self.ax1) = self.plt.subplots(1, 2, figsize=(10, 5))

        self.lines, = self.ax.plot([],[], 'o')
        self.lines1, = self.ax1.plot([],[], 'o')

        self.ax.set_xlim(0, self.pltMax + 6)
        self.ax.set_ylim(0, self.pltMax + 6)

        self.ax1.set_xlim(0, self.pltMax + 6)
        self.ax1.set_ylim(0, self.pltMax + 6)
        
        self.ax.grid()
        self.ax1.grid()
       
        self.populate()

    def setTitle(self,handle,title):
        handle.title.set_text(title)

    def setText(self, handle, text):
        handle.text(1, (self.pltMax+3), text, fontsize=8)

    def getHandle(self):
        return self.ax, self.ax1

    def updateSet(self):
        self.lines.set_data(self.xdata, self.ydata)
        self.lines1.set_data(self.xdata, self.ydata)
        #self.plt.pause(0.001)
        self.updateFigure()

    def populate(self):
        for x in range(0, self.pltCount):
            self.xdata.append(random.randint(self.pltMin, self.pltMax))
            self.ydata.append(random.randint(self.pltMin, self.pltMax))
        self.updateSet()

    def connectDots(self, pt1, pt2, handle, color):
        x1, x2 = pt1[0], pt2[0]
        y1, y2 = pt1[1], pt2[1]
        lineId = self.id
        line = handle.plot([x1,x2], [y1,y2], color, gid = lineId)
        self.id += 1
        self.updateFigure()
        return lineId
    
    def updateFigure(self):
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def deleteConnection(self, gid):
        for i in self.ax.lines:
            if i.get_gid() == gid:
                i.remove()
                break

    def removeOldLines(self, handle, toKeep = 1):
        del handle.lines[toKeep:]
        self.updateSet()

    def removeNewestLine(self, handle):
        del handle.lines[-1]
        self.updateSet()

    def getStart(self):
        return self.start

    def getData(self):
        return self.xdata, self.ydata

    def calculateDist(self, p1, p2):
        return math.sqrt((math.pow((p2[0] - p1[0]), 2)) + math.pow((p2[1] - p1[1]), 2))

class TSPGreedy():
    basicColor = "b--"
    bestColor = "r-"
    def __init__(self, canvas, handle):
        self.problemCanvas = canvas
        self.handle = handle
        self.problemCanvas.setTitle(self.handle, "Greedy Algorithm")

        self.problemCanvas.removeOldLines(self.handle)
        self.totalDistance = 0

    def performAlgo(self):
        self.start = self.problemCanvas.getStart()
        data = self.problemCanvas.getData()
        self.XCord = data[0]
        self.YCord = data[1]
        self.data = []
        for i in range(1, len(self.XCord)):
            self.data.append((self.XCord[i], self.YCord[i]))

        nextPoint = self.smallestDistance(self.start, self.data)
        self.problemCanvas.connectDots(self.start, nextPoint, self.handle, self.bestColor)
        self.data.remove(nextPoint)
        path =[self.start, nextPoint]

        while self.data != []:
            prevPoint = nextPoint
            nextPoint = self.smallestDistance(prevPoint, self.data)
            path.append(nextPoint)
            self.problemCanvas.connectDots(prevPoint, nextPoint, self.handle, self.bestColor)
            self.data.remove(nextPoint)
            
        conclusionStr = "Total Distance: " + str(self.totalDistance) + "\nPath: " + str(path)
        self.problemCanvas.setText(self.handle, conclusionStr)
        return path


    def smallestDistance(self, pt, data):
        minimum = 999
        retPt = None
        for i in data:
            self.problemCanvas.connectDots(pt, i, self.handle, self.basicColor)            
            curMin = self.problemCanvas.calculateDist(pt, i)
            if  curMin < minimum:
                minimum = curMin
                retPt = i
            self.problemCanvas.removeNewestLine(self.handle)            

        self.totalDistance += minimum
        return retPt
            

class TSPBruteForce(threading.Thread):
    basicColor = "b--"
    bestColor = "r-"
    def __init__(self, problemCanvas, handle):
        self.canvas = problemCanvas
        self.handle = handle
        self.canvas.setTitle(self.handle, "Brute Force Algorithm")

        self.canvas.removeOldLines(self.handle)
        data = problemCanvas.getData()
        start = self.canvas.getStart()

        self.XCord = data[0]
        self.YCord = data[1]
        self.AllCord = []
        self.weights = {}
        self.path = {}

        for i in range(0, len(self.XCord)):
            self.AllCord.append((self.XCord[i], self.YCord[i]))
        self.allToTry = list(itertools.permutations(self.AllCord[1:]))
        for i in range(0, len(self.allToTry)):
            self.allToTry[i] = (start,) + self.allToTry[i]

    def performAlgo(self):
        minimum = 999
        bestSet = None
        for perm in self.allToTry:
            distance = 0
            self.path[perm] = []
            distance = self.iterThroughPerm(perm, self.basicColor)
            self.weights[perm] = distance
            self.canvas.removeOldLines(self.handle)
            if distance < minimum:
                minimum = distance
                bestSet = perm

        self.iterThroughPerm(bestSet, self.bestColor)
        conclusionStr = "Total Distance: " + str(minimum) + "\nPath: " + str(bestSet)
        self.canvas.setText(self.handle, conclusionStr)
        return bestSet

    def iterThroughPerm(self, perm, color):
        accmulDistance = 0
        for i in range(1, len(perm)):
            accmulDistance += self.canvas.calculateDist(perm[i - 1], perm[i])
            lineId = self.canvas.connectDots(perm[i - 1], perm[i], self.handle, color)
            self.path[perm].append(lineId)
        return accmulDistance
                    

problem = plotCompareProblem(5)
handle, handle1 = problem.getHandle()

T = TSPGreedy(problem, handle1)
T1 = TSPBruteForce(problem, handle)

T.performAlgo()
T1.performAlgo()
