from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *

import sys
import random
import warnings

from plot2        import *
from plotWidgets  import *
from dataMenu     import *
from plotMenu     import *
from annMenu      import *
from extrapMenu   import *
from calculations import *

import numpy as np

warnings.filterwarnings("ignore")

class main(QWidget):
    def __init__(self, data=[0]):
        QWidget.__init__(self)

        #Style window
        self.setStyleSheet("background-color: black; border: 1px solid white")

        #Set layout to grid
        self.setLayout(QGridLayout())

        #Define data as class variable
        self.data = data 

        #Call function to re-format a 1D list into a 2D list
        self.fillXVals()

        #Set boolean variables for whether to annotate, show labels, etc.
        self.hYMax = False
        self.hYMin = False

        self.hXMax = False
        self.hXMin = False

        self.showMean = False

        self.showPmccLabel = False
        self.showSrccLabel = False

        self.xOnY = 2
        self.yOnX = 0

        self.reg = "xOnY"

        self.showPolReg = 0
        self.showLinReg = 0
        self.showExpReg = 0

        self.polRegOrd = 0

        #Find minimum and maximum x values
        self.minExtrapVal = min(self.data[0])
        self.maxExtrapVal = max(self.data[0])

        self.regStr = 0

        #Get screenwidth and screenheight
        self.screenWidth  = self.geometry().width()
        self.screenHeight = self.geometry().height()

        self.initUI(self.data)

        self.showMaximized()

    def initUI(self, data):
        self.data = data

        #Cut off data if one data set is longer then the other
        if len(self.data[0]) != len(self.data[1]):
            self.data = [self.data[0][:min(len(self.data[0]), len(self.data[1]))],
                         self.data[1][:min(len(self.data[0]), len(self.data[1]))]]

        #If there's no data, clear the plot
        if self.data[0] == [] and self.data[1] == []:
            self.plotWidget.plot.clear()
            return

        #Create calculations class for data. Used to calculate pmcc and srcc
        self.calculations = calculations(self.data)

        #Create list of menu names and menu classes
        self.menuText = ["Data", "Regressions", "Calculations", "Annotations", "Extrapolation"]
        self.menus    = [dataMenu, regMenu, calcMenu, annMenu, extrapMenu]

        #Create plot for data
        self.plotWidget = plot(self, self.data)

        #Add plot and menu to layout
        self.layout().addWidget(self.plotWidget, 0, 0)
        self.layout().addWidget(plotMenu(self), 0, 1)

        #Show plots if they were previously shown and data was changed
        if   self.showPolReg: self.plotPolReg(self.order)
        elif self.showLinReg: self.plotLinReg()
        elif self.showExpReg: self.plotExpReg()

        #Show pmcc and srcc labels if they were previously shown
        if self.showPmccLabel: self.showPmcc()
        if self.showSrccLabel: self.showSrcc()

        #Show annotations. Whether they need to be shown or not is decided within the function
        self.showAnnotations()

    #Procedure to reformat 1D data into 2D data
    def fillXVals(self):

        #If first element of data isn't a list
        if type(self.data[0]) != list:

            #Copy data
            temp = self.data.copy()

            #Define data as 2D list
            self.data = [[],[]]

            #Loop though data copy
            for i in range(len(temp)):

                #Append the index to x values
                self.data[0].append(i)

                #Append 1D data values to y values
                self.data[1].append(temp[i])

    #Procedure to show equation of regression line
    def showRegEq(self):
        #Get string containing equation with rounded values
        regStr = self.plotWidget.roundedRegStr

        #Format string from text into CSS format
        regStr = regStr.replace("**", "<sup>")
        regStr = regStr.replace("+", "</sup>+")
        regStr = regStr.replace("+-", "-")
        regStr = regStr.replace("*", "")
        regStr = regStr.replace("2.7183", "e")
        regStr = regStr.replace("+", " + ")
        regStr = regStr.replace("-", " - ")
        regStr = regStr.replace("x<sup>0</sup>", "")
        regStr = regStr.replace("x<sup>1</sup>", "x")

        #Create draggable label containing the equation
        self.regLabel = draggablePlotLabel(self, text=regStr)

        #Align the text to the centre of the label and show the label
        self.regLabel.setAlignment(Qt.AlignCenter)
        self.regLabel.show()

    #Abstract procedure to show any menu
    def showMenu(self, menu):

        #Create menu widget based on menu parsed
        menu = menu(self)

        #Move menu widget to middle of screen
        menu.move(QPoint(self.screenWidth//2,
                         self.screenHeight//2))

        #Make menu minimum size
        menu.setFixedSize(QSize(menu.minimumSize()))

        #Show menu
        menu.show()

    #Procedure to bring widget to front
    def raiseWidget(self, widget):
        try:
            widget.raise_()
            widget.activateWindow()
        except:
            pass

    ##Regressions##

    #Procedure to remove all plotted lines
    def clearLines(self):
        self.showLinReg = 0
        self.showPolReg = 0
        self.showExpReg = 0

        #Try to remove lines/curves and equation label from plot 
        try:    self.plotWidget.plot.removeItem(self.plotWidget.line)
        except: pass

        try:    self.plotWidget.plot.removeItem(self.plotWidget.curve)
        except: pass

        try:    self.regLabel.deleteLater()
        except: pass

    #Procedure to plot linear regression
    def plotLinReg(self, reg):
        if reg == "xOnY":
            self.xOnY = 2
            self.yOnX = 0
        elif reg == "yOnX":
            self.xOnY = 0
            self.yOnX = 2

        #Clear plot
        self.clearLines()

        #Plot linear regression
        self.plotWidget.linReg(reg)

        #Show equation laebl
        self.showRegEq()

        #Set variable determining state of linear regression checkbox to 2
        self.showLinReg = 2

        #Store non-rounded equation into class variable
        self.regStr = self.plotWidget.regStr

    #Procedure to plot polynomial regression
    def plotPolReg(self, order=None):

        #Store parsed order into calss variable
        self.order = order

        #If no order was parsed, set order to 5
        if self.order == None:
            self.order = 5

        #Clear plot
        self.clearLines()

        #Plot polynomial regression using order parsed
        self.plotWidget.polReg(self.order)

        #Show equation label
        self.showRegEq()

        #Set variable determining state of polynomial regression checkbox to 2
        self.showPolReg = 2

        #Store order into class variable
        self.polRegOrd  = self.order

        #Store non-rounded equation into class variable
        self.regStr = self.plotWidget.regStr

    #Procedure to plot exponential regression
    def plotExpReg(self):

        #Clear plot
        self.clearLines()

        #Plot exponential regression
        self.plotWidget.expReg()

        #Show equation label
        self.showRegEq()

        #Set variable determining state of exponential regression checkbox to 2
        self.showExpReg = 2

        #Store non-rounded equation into class variable
        self.regStr = self.plotWidget.regStr

    ##Calculations##

    #Procedure to show pmcc label
    def showPmcc(self):

        #Create label containing pmcc
        self.pmccLabel = draggablePlotLabel(self, text="PMCC = " + str(self.calculations.pmcc()))

        #Show label
        self.pmccLabel.show()

        #Set variable determining whether the label is visible or not to 2
        self.showPmccLabel = 2

    #Procedure to show srcc label
    def showSrcc(self):

        #Create label containing srcc
        self.srccLabel = draggablePlotLabel(self, text="SRCC = " + str(self.calculations.srcc()))

        #Show label
        self.srccLabel.show()

        #Set variable determining whether the label is visible or not to 2
        self.showSrccLabel = 2

    ##Annotations##
        
    #Annotate plot based on user input
    def showAnnotations(self, hYMax=False, hYMin=False, hXMax=False, hXMin=False, showMean=False):
        self.hYMax    = hYMax
        self.hYMin    = hYMin
        self.hXMax    = hXMax
        self.hXMin    = hXMin
        self.showMean = showMean
        self.plotWidget.annotate(hYMax, hYMin, hXMax, hXMin, showMean)

    ##Extrapolation##

    #Procedure to set variable containing minimum value and plot it
    def plotExtrapMin(self, minVal):
        self.minExtrapVal = minVal

        self.plotExtrap()

    #Procedure to set variable containing maximum value and plot it
    def plotExtrapMax(self, maxVal):
        self.maxExtrapVal = maxVal

        self.plotExtrap()

    #Procedure to plot data
    def plotExtrap(self):

        #Create plot widget
        self.plotWidget = plot(self, self.data)

        #Set minimum and maximum values of the plot
        self.plotWidget.minExtrapVal = self.minExtrapVal
        self.plotWidget.maxExtrapVal = self.maxExtrapVal 

        #Plot data
        self.plotWidget.plotCurve(self.regStr, self.data[0], self.data[1])

        #Annotate if necessary
        self.plotWidget.annotate(hYMax = self.hYMax, hYMin = self.hYMin, hXMax = self.hXMax, hXMin = self.hXMin, showMean = self.showMean)

        #Delete previous plot, and show new plot
        self.layout().itemAtPosition(0, 0).widget().deleteLater()
        self.layout().addWidget(self.plotWidget, 0, 0)

        #If the labels were shown before extrapolating, make sure they are now
        try:
            self.raiseWidget(self.regLabel)
            self.raiseWidget(self.pmccLabel)
            self.raiseWidget(self.srccLabel)
        except:
            pass
        

app = QApplication(sys.argv)

data1 = [[-5, -4, -3, -2, -1],
        [3, 7, 20, 54, 148]]

data1[1].reverse()

##data = [[1, 1, 3, 3],
##        [1, 3, 1, 3]]

data = [1,5,6,2,3,7,8,4,2,2,1]#[1,5,6,2,3,2,8,7,6,9,4,6,3]]

m = main(data)

app.exec_()
