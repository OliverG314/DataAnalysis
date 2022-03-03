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

        #Style window
        self.setStyleSheet("background-color: black")

        #Set layout to vertical box layout
        self.setLayout(QVBoxLayout())

        self.data = data

        #Find mean of x and y data sets
        self.meanX = sum(data[0])/len(data[0])
        self.meanY = sum(data[1])/len(data[1])

        #Find min and max x values
        self.minExtrapVal = min(self.data[0])
        self.maxExtrapVal = max(self.data[0])

        #Create lists to contain text items showing min/max x/y values
        self.maxYTextList = []
        self.minYTextList = []

        self.maxXTextList = []
        self.minXTextList = []

        #Create text item showing mean point
        self.meanPointText = pg.TextItem("Mean point = (" + str(self.meanX) + ", " + str(self.meanY) + ")", anchor=(0,0))

        #Loop through data
        for i in range(len(self.data[0])):

            #Check if current y value = the maximum y value
            if self.data[1][i] == max(self.data[1]):

                #Append text item showing the max values to the corresponding list
                self.maxYTextList.append(pg.TextItem("Max Y = (" + str(self.data[0][i]) + ", " + str(self.data[1][i]) + ")", anchor=(0,0)))
            elif self.data[1][i] == min(self.data[1]):
                self.minYTextList.append(pg.TextItem("Min Y = (" + str(self.data[0][i]) + ", " + str(self.data[1][i]) + ")", anchor=(0,0)))

            if self.data[0][i] == max(self.data[0]):
                self.maxXTextList.append(pg.TextItem("Max X = (" + str(self.data[0][i]) + ", " + str(self.data[1][i]) + ")", anchor=(1,1)))
            if self.data[0][i] == min(self.data[0]):
                self.minXTextList.append(pg.TextItem("Min X = (" + str(self.data[0][i]) + ", " + str(self.data[1][i]) + ")", anchor=(1,1)))

        #Create plot widget
        self.plot = pg.PlotWidget()

        #Add plot to layout
        self.layout().addWidget(self.plot)

        #Plot data points
        self.scatterPlot()

    #Procedure for linear regression with optional parameter for whether to regress x on y, or y on x
    def linReg(self, reg="xOnY"):
        #Number of data points
        n = len(self.data[0])

        #Sum of x and y values
        x = sum(self.data[0])
        y = sum(self.data[1])

        #Calculate mean values of x and y
        xBar = sum(self.data[0])/len(self.data[0])
        yBar = sum(self.data[1])/len(self.data[1])

        #Sum of x values * y values
        xy = sum([self.data[0][i] * self.data[1][i] for i in range(len(self.data[0]))])

        #Sum of x values squared
        x2 = sum([self.data[0][i]**2 for i in range(len(self.data[0]))])
        y2 = sum([self.data[1][i]**2 for i in range(len(self.data[1]))])

        #Calculate Sxy, Sxx, and Syy
        Sxy = xy - n*xBar*yBar
        Sxx = x2 - n*xBar**2
        Syy = y2 - n*yBar**2

        #Gradient and y-intercept
        #Check whether the user wishes to regress x on y, or y on x
        if reg == "xOnY":
            self.m = Sxy/Sxx
            self.c = yBar - self.m*xBar
            
            #Uses x values to calculate y values using new function
            #Function: y = mx+c
            xVals = self.data[0]
            yVals = [self.m*self.data[0][i] + self.c for i in range(len(self.data[0]))]
        elif reg == "yOnX":
            self.m = Sxy/Syy
            self.c = xBar - self.m*yBar

            #Uses x values to calculate y values using new function
            #Function: x = my+c. Rearranged to y = (x-c)/m
            xVals = self.data[0]
            yVals = [(self.data[0][i] - self.c)/self.m for i in range(len(self.data[0]))]

        #Create line plot item
        self.line = pg.PlotDataItem(xVals, yVals, connect="all")

        #Store non-rounded equation into class variable
        self.regStr = str(self.c) + str(self.m) + "*x**1"

        #Store rounded equation into class variable
        self.roundedRegStr = str(round(self.c, 4)) + str(round(self.m, 4)) + "x**1"

        #Add line to main plot
        self.plot.addItem(self.line)

    #Procedure for polynomial regressions, with parameter for order
    def polReg(self, order):
        
        #Store x and y data sets into local variables
        x = self.data[0]
        y = self.data[1]
        
        #String that stores polynomial
        regStr = ""

        #String that stores rounded polynomial
        roundedRegStr = ""

        #Create matrix to store x values raised to increasing powers across columns
        xMatrix = []

        #Loop through all x values
        #First  row = x_1**0, x_1**1, x_1**2
        #Second row = x_2**0, x_2**1, ...
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

        #Plot data
        self.plotCurve(self.regStr, x, y)

    #Procedure for exponential regressions
    #Find me a buggier procedure lol
    def expReg(self):

        #Store x and y data sets into local variables
        x = self.data[0]
        y = self.data[1]

        #Sign of base and exponenent
        baseSign = 1
        expSign  = 1

        #How much function needs to be moved by
        xShift = 0
        yShift = 0

        #Meant to work out sign of exponent
        if x[0] > x[-1]:
            expSign = -1
        elif x[0] < x[-1]:
            expSign = 1

        #Move y values above x axis and store how much it has moved by
        while min(y) < 1:
            for i in range(len(y)):
                y[i] += 1
            yShift += 1

        #Move x values to the right of y axis and store how much it has moved
        while min(x) < 1:
            for i in range(len(x)):
                x[i] += 1
            xShift += 1

        #Take the log of each list
        logX = [log(i) for i in x]
        logY = [log(i) for i in y]

        #Create plot for log of data
        #Isn't displayed
        logPlot = plot(self, [x, logY])

        #Secretly plot the logged data
        logPlot.linReg()

        #Get the gradient and y-intercept of the logged data
        logPlotM = logPlot.m
        logPlotC = logPlot.c

        #Do this
        xShift = e**xShift

        #Store non-rounded equationn into class variable, multiplying by xShift to move left and adding yShift to move down
        self.regStr = str(xShift) + "*" + str(baseSign) + "*" + str(e) + "**" + str(logPlotC) + "*" + str(e) + "**(" + str(expSign) + "*" + str(logPlotM) + "*x)-" + str(yShift)

        #Store rounded equationn into class variable, multiplying by xShift to move left and adding yShift to move down
        self.roundedRegStr = str(xShift) + "*" + str(baseSign) + "*" + str(round(e, 4)) + "**" + str(round(logPlotC, 4)) + "</sup>*" + str(round(e, 4)) + "**("  + str(expSign) + "*" + str(round(logPlotM, 4)) + "*x)</sup>-" + str(yShift)

        #Plot data
        self.plotCurve(self.regStr, x, y)

    #Procedure to plot data
    def plotCurve(self, eq, x, y, interpXScale = 2500):
        #Create list from minimum value to maximum value but with smaller steps
        xVals = list(np.linspace(self.minExtrapVal, self.maxExtrapVal, interpXScale))
        yVals = []

        #Substitute x values into polynomial string and evaluate its value
        for i in xVals:
            try:    yVals.append(eval(eq.replace("x", "(" + str(i) + ")")))
            except: yVals.append(eval(eq.replace("x", str(i))))

        #Create curve
        self.curve = pg.PlotDataItem(xVals, yVals, connect="all")

        #Add curve to main plot
        self.plot.addItem(self.curve)

    #Function to set text for min/max of x/y and plot the point with the text and color the point
    def getPoint(self, xy, maxMin, count, x, y, i):
        if xy == "x":
            if maxMin == "max":
                text = self.maxXTextList[count]
            elif maxMin == "min":
                text = self.minXTextList[count]
                
        elif xy == "y":
            if maxMin == "max":
                text = self.maxYTextList[count]
            elif maxMin == "min":
                text = self.minYTextList[count]

        text.setPos(x, y)

        self.plot.addItem(text)

        point = {"pos":   [self.data[0][i], self.data[1][i]],
                 "brush": pg.mkBrush((0, 25, 255)),
                 "size":  10}

        return point

    #Procedure to remove all items in parsed list
    def removeAll(self, itemList):
        for i in itemList:
            self.plot.removeItem(i)

    #Procedure to plot data points
    def scatterPlot(self):

        #Create list to contain points
        pointsList = []

        #Create scatter plot
        self.scatter = pg.ScatterPlotItem()

        #Loop through data
        for i in range(len(self.data[0])):

            #Create point
            point = {"pos":   [self.data[0][i], self.data[1][i]],
                     "brush": pg.mkBrush((0, 255, 25)),
                     "size": 10}

            #Append point to list
            pointsList.append(point)

        #Add points to scatter plot
        self.scatter.addPoints(pointsList)

        #Add scatter plot to main plot
        self.plot.addItem(self.scatter)

    #Procedure to add text where necessary
    #No. I didn't comment it. I didn't want to.
    def annotate(self, hYMax=False, hYMin=False, hXMax=False, hXMin=False, showMean=False):
        maxYCount = 0
        minYCount = 0
        maxXCount = 0
        minXCount = 0

        self.scatter.setBrush(pg.mkBrush((0, 255, 25)))
        
        for i in range(len(self.data[0])):
            if (self.data[1][i] == max(self.data[1])):
                if hYMax:
                    point = self.getPoint("y", "max", maxYCount, self.data[0][i], self.data[1][i], i)

                    maxYCount += 1
                else:
                    self.removeAll(self.maxYTextList)
                        
            if (self.data[1][i] == min(self.data[1])):
                if hYMin:
                    point = self.getPoint("y", "min", minYCount, self.data[0][i], self.data[1][i], i)
                    
                    minYCount += 1
                else:
                    self.removeAll(self.minYTextList)

            if (self.data[0][i] == max(self.data[0])):
                if hXMax:
                    point = self.getPoint("x", "max", maxXCount, self.data[0][i], self.data[1][i], i)

                    maxXCount += 1
                else:
                    self.removeAll(self.maxXTextList)

            if (self.data[0][i] == min(self.data[0])):
                if hXMin:
                    point = self.getPoint("x", "min", minXCount, self.data[0][i], self.data[1][i], i)

                    minXCount += 1
                else:
                    self.removeAll(self.minXTextList)

        self.meanPoint = {"pos": [self.meanX,self.meanY],
                          "brush": pg.mkBrush((255, 0, 0)),
                          "size": 10}

        if showMean:
            self.scatter.addPoints([self.meanPoint])
            self.meanPointText.setPos(self.meanX, self.meanY)
            self.plot.addItem(self.meanPointText)            
        else:
            try:
                self.window().plotWidget.scatter.setData(self.data[0],
                                                         self.data[1])
                self.plot.removeItem(self.meanPointText)
                
            except:
                pass

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
