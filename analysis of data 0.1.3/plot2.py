from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *

import pyqtgraph as pg

import sys
from math import log, e

import numpy as np
from scipy.interpolate import interp1d

class plot(QWidget):
    def __init__(self, parent, data):
        QWidget.__init__(self, parent)

        self.setStyleSheet("background-color: black")
        self.setLayout(QVBoxLayout())

        self.data = data

        self.minExtrapVal = min(self.data[0])
        self.maxExtrapVal = max(self.data[0])

        self.maxYTextList = []
        self.minYTextList = []

        self.maxXTextList = []
        self.minXTextList = []

        for i in range(len(self.data[0])):
            if self.data[1][i] == max(self.data[1]):
                self.maxYTextList.append(pg.TextItem("Max Y = (" + str(self.data[0][i]) + ", " + str(self.data[1][i]) + ")", anchor=(0,0)))
            elif self.data[1][i] == min(self.data[1]):
                self.minYTextList.append(pg.TextItem("Min Y = (" + str(self.data[0][i]) + ", " + str(self.data[1][i]) + ")", anchor=(0,0)))

            if self.data[0][i] == max(self.data[0]):
                self.maxXTextList.append(pg.TextItem("Max X = (" + str(self.data[0][i]) + ", " + str(self.data[1][i]) + ")", anchor=(1,1)))
            if self.data[0][i] == min(self.data[0]):
                self.minXTextList.append(pg.TextItem("Min X = (" + str(self.data[0][i]) + ", " + str(self.data[1][i]) + ")", anchor=(1,1)))
        
        self.plot = pg.PlotWidget()

        self.layout().addWidget(self.plot)
            
        self.scatterPlot()

    def linReg(self):
        #Number of data points
        n = len(self.data[0])

        #Sum of x and y values
        x = sum(self.data[0])
        y = sum(self.data[1])

        #Sum of x values * y values
        xy = sum([self.data[0][i] * self.data[1][i] for i in range(len(self.data[0]))])

        #Sum of x values squared
        x2 = sum([self.data[0][i]**2 for i in range(len(self.data[0]))])

        #Gradient and y-intercept
        self.m = (n*xy - x*y)/(n*x2 - x**2)
        self.c = (y - self.m*x)/n

        #Using x values to plot y values using new function
        xVals = self.data[0]
        yVals = [self.m*self.data[0][i] + self.c for i in range(len(self.data[0]))]

        #Create line plot item
        self.line = pg.PlotDataItem(xVals, yVals, connect="all")

        self.regStr = str(self.c) + str(self.m) + "x**1"

        self.roundedRegStr = str(round(self.c, 4)) + str(round(self.m, 4)) + "x**1"

        #Add line to main plot
        self.plot.addItem(self.line)

    def polReg(self, order):
        x = self.data[0]
        y = self.data[1]
        
        #String that stores polynomial
        regStr = ""

        #String that stores rounded polynomial
        roundedRegStr = ""

        #Detail of interpolation
        interpXScale = 100

        #Create matrix to store x values raised to increasing powers across columns
        xMatrix = []

        #Loop through all x values
        #First  row = x1**0, x1**1, x1**2
        #Second row = x2**0, x2**1, ...
        for i in range(len(x)):
            row = []

            for j in range(order+1):
                row.append(x[i]**j)

            xMatrix.append(row)

        #Convert 2d array to matrix then invert it
        xMatrix  = np.matrix(xMatrix, dtype="float64")
        xMatrixI = xMatrix.I

        #Store all y values of vector
        yMatrix = y

        #Multiply y values vector by x values matrix
        coeffs = np.matmul(xMatrixI, yMatrix)

        #Convert from numpy matrix to list of floats representing coefficients
        items = [coeffs.item(i) for i in range(coeffs.size)]

        #Loop through all coefficents 
        for i in items:
            
            #Multiply coefficients by increasing powers of x
            regStr += str(i) + "*x**" + str(items.index(i)) + "+"

            #Do the same but round them for displaying
            roundedRegStr += str(round(i, 4)) + "*x**" + str(items.index(i)) + "+"

        #Remove the last "+"
        self.regStr = regStr[:-1]

        #Remove the last "+"
        self.roundedRegStr = roundedRegStr[:-1]

        self.plotCurve(self.regStr, x, y)

    def expReg(self):
        x = self.data[0]
        y = self.data[1]

        try: x[x.index(0)] = 1
        except: pass

        try: y[y.index(0)] = 1
        except: pass

        logX = [log(i) for i in x]
        logY = [log(i) for i in y]

        logPlot = plot(self, [x, logY])

        logPlot.linReg()

        logPlotM = logPlot.m
        logPlotC = logPlot.c

        a = e ** logPlotM
        b = e ** logPlotC

        self.regStr = str(e) + "**" + str(logPlotC) + "*" + str(e) + "**(" + str(logPlotM) + "*x)"

        self.roundedRegStr = str(round(e, 4)) + "**" + str(round(logPlotC, 4)) + "</sup>*" + str(round(e, 4)) + "**" + str(round(logPlotM, 4)) + "*x"

        self.plotCurve(self.regStr, x, y)

    def plotCurve(self, eq, x, y, interpXScale = 100, exp=0):
        xVals = list(np.linspace(self.minExtrapVal, self.maxExtrapVal, 2000))
        yVals = []

        #Substitute x values into polynomial string and evaluate its value
        for i in xVals:
            yVals.append(eval(eq.replace("x", "(" + str(i) + ")")))

        #Create curve
        self.curve = pg.PlotDataItem(xVals, yVals, connect="all")

        #Add curve to main plot
        self.plot.addItem(self.curve)

    def textLabel(self, xy, maxMin, count, x, y, i):
        if xy == "x":
            if maxMin == "max":
                brush = (150, 150, 25)

                text = self.maxXTextList[count]
            elif maxMin == "min":
                brush = (25, 150, 150)

                text = self.minXTextList[count]
        elif xy == "y":
            if maxMin == "max":
                brush = (255, 0, 25)

                text = self.maxYTextList[count]
            elif maxMin == "min":
                brush = (0, 25, 255)

                text = self.minYTextList[count]

        text.setPos(x, y)

        self.plot.addItem(text)

        point = {"pos":    [self.data[0][i], self.data[1][i]],
                 "brush":  pg.mkBrush(brush)}

        return point

    def removeAll(self, itemList):
        for i in itemList:
            self.plot.removeItem(i)

    def scatterPlot(self, hYMax=False, hYMin=False, hXMax=False, hXMin=False):
        pointsList = []

        self.scatter = pg.ScatterPlotItem()

        maxYCount = 0
        minYCount = 0
        maxXCount = 0
        minXCount = 0
        
        for i in range(len(self.data[0])):            
            point = {"pos":   [self.data[0][i], self.data[1][i]],
                     "brush": pg.mkBrush((0, 255, 25))}

            if (self.data[1][i] == max(self.data[1])):
                if hYMax:
                    point = self.textLabel("y", "max", maxYCount, self.data[0][i], self.data[1][i], i)

                    maxYCount += 1
                else:
                    self.removeAll(self.maxYTextList)
                        
            if (self.data[1][i] == min(self.data[1])):
                if hYMin:
                    point = self.textLabel("y", "min", minYCount, self.data[0][i], self.data[1][i], i)
                    
                    minYCount += 1
                else:
                    self.removeAll(self.minYTextList)

            if (self.data[0][i] == max(self.data[0])):
                if hXMax:
                    point = self.textLabel("x", "max", maxXCount, self.data[0][i], self.data[1][i], i)

                    maxXCount += 1
                else:
                    self.removeAll(self.maxXTextList)

            if (self.data[0][i] == min(self.data[0])):
                if hXMin:
                    point = self.textLabel("x", "min", minXCount, self.data[0][i], self.data[1][i], i)

                    minXCount += 1
                else:
                    self.removeAll(self.minXTextList)

            pointsList.append(point)

        self.scatter.addPoints(pointsList)

        #Add scatter plot to main plot
        self.plot.addItem(self.scatter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    data = [[1, 2, 3, 4,5,6,7,8,9,10,11,12,13],
            [20,13,10,8,7,7,5,5,4,3, 1, 1, 25]]
##    data = [[0.001, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21],
##            [1, 1.03, 1.06, 1.38, 2.09, 3.54, 6.41, 12.6, 22.1, 39.05, 65.32, 99.78]]
        
    p = plot(None, data)
    p.expReg()
    p.showMaximized()
    app.exec_()
