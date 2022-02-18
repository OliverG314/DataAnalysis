from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *

import sys
import random
import warnings

from plot2           import *
from plotWidgets     import *
from plotMenu        import *
from annMenu         import *
from extrapMenu      import *
from calculations    import *

import numpy as np

warnings.filterwarnings("ignore")

class main(QWidget):
    def __init__(self, data=[0]):
        QWidget.__init__(self)

        self.setStyleSheet("background-color: black; border: 1px solid white")
        self.setLayout(QGridLayout())
        
        self.data = data

        self.hYMax = False
        self.hYMin = False

        self.hXMax = False
        self.hXMin = False

        self.showMean = False

        self.showPmccLabel = False
        self.showSrccLabel = False

        self.showPolReg = 0
        self.showLinReg = 0
        self.showExpReg = 0

        self.polRegOrd = 0

        self.minExtrapVal = min(self.data[0])
        self.maxExtrapVal = max(self.data[0])

        self.regStr = 0

        self.screenWidth  = self.geometry().width()
        self.screenHeight = self.geometry().height()

        self.initUI(self.data)

        self.showMaximized()

    def initUI(self, data):
        self.data = data
        
        self.fillXVals()

        self.calculations = calculations(self.data)

        self.menuText = ["Regressions", "Calculations", "Annotations", "Extrapolation"]
        self.menus    = [regMenu, calcMenu, annMenu, extrapMenu]

        self.plotWidget = plot(self,
                               self.data)

        self.layout().addWidget(self.plotWidget, 1, 1)
        self.layout().addWidget(plotMenu(self), 1, 2)

    def fillXVals(self):
        if type(self.data[0]) != list:
            temp = self.data

            self.data = [[],[]]

            for i in range(len(temp)):
                self.data[0].append(i)
                self.data[1].append(temp[i])

    def showRegEq(self):
        regStr = self.plotWidget.roundedRegStr

        regStr = regStr.replace("**", "<sup>")
        regStr = regStr.replace("+", "</sup>+")
        regStr = regStr.replace("+-", "-")
        regStr = regStr.replace("*", "")
        regStr = regStr.replace("2.7183", "e")
        regStr = regStr.replace("+", " + ")
        regStr = regStr.replace("-", " - ")
        regStr = regStr.replace("x<sup>0</sup>", "")
        regStr = regStr.replace("x<sup>1</sup>", "x")
        
        self.regLabel = draggablePlotLabel(self, text=regStr)
        
        self.regLabel.setAlignment(Qt.AlignCenter)
        self.regLabel.show()

        self.eq = 2

    def showMenu(self, menu):
        menu = menu(self)

        menu.move(QPoint(self.screenWidth//2,
                         self.screenHeight//2))

        menu.setFixedSize(QSize(menu.minimumSize()))

        menu.show()

    def raiseWidget(self, widget):
        try:
            widget.raise_()
            widget.activateWindow()
        except:
            pass

    ##Regressions##
    def clearLines(self):
        self.showLinReg = 0
        self.showPolReg = 0
        self.showExpReg = 0
        
        try:    self.plotWidget.plot.removeItem(self.plotWidget.line)
        except: pass

        try:    self.plotWidget.plot.removeItem(self.plotWidget.curve)
        except: pass

        try:    self.regLabel.deleteLater()
        except: pass

    def plotLinReg(self):
        self.clearLines()
        
        self.plotWidget.linReg()

        self.showRegEq()

        self.showLinReg = 2

        self.regStr = self.plotWidget.regStr

    def plotPolReg(self, order=None):
        self.order = order
        
        if self.order == None:
            self.order = 10
            
        self.clearLines()
        
        self.plotWidget.polReg(self.order)

        self.showRegEq()

        self.showPolReg = 2
        self.polRegOrd  = self.order

        self.regStr = self.plotWidget.regStr

    def plotExpReg(self):
        self.clearLines()

        self.plotWidget.expReg()

        self.showRegEq()

        self.showExpReg = 2

        self.regStr = self.plotWidget.regStr

    ##Calculations##
    def showPmcc(self):
        self.pmccLabel = draggablePlotLabel(self, text="PMCC = " + str(self.calculations.pmcc()))

        self.pmccLabel.show()

        self.showPmccLabel = 2

    def showSrcc(self):
        self.srccLabel = draggablePlotLabel(self, text="SRCC = " + str(self.calculations.srcc()))

        self.srccLabel.show()

        self.showSrccLabel = 2

    ##Annotations##
    def highlightMaxY(self, hMax=False):
        self.hYMax = hMax

        self.showAnnotations()

    def highlightMinY(self, hMin=False):
        self.hYMin = hMin

        self.showAnnotations()
        
    def highlightMaxX(self, hMax=False):
        self.hXMax = hMax

        self.showAnnotations()

    def highlightMinX(self, hMin=False):
        self.hXMin = hMin

        self.showAnnotations()

    def showMeanPoint(self, showMean=False):
        self.showMean = showMean

        self.showAnnotations()

    def showAnnotations(self):
        self.plotWidget.annotate(hYMax = self.hYMax, hYMin = self.hYMin, hXMax = self.hXMax, hXMin = self.hXMin, showMean = self.showMean)

    ##Extrapolation##
    def plotExtrapMin(self, minVal):
        self.minExtrapVal = minVal

        self.plotExtrap()

    def plotExtrapMax(self, maxVal):
        self.maxExtrapVal = maxVal

        self.plotExtrap()

    def plotExtrap(self):
        self.plotWidget = plot(self, self.data)

        self.plotWidget.minExtrapVal = self.minExtrapVal
        self.plotWidget.maxExtrapVal = self.maxExtrapVal 

        if self.showExpReg == 2: self.plotWidget.plotCurve(self.regStr, self.data[0], self.data[1], exp=1)
        else:self.plotWidget.plotCurve(self.regStr, self.data[0], self.data[1], exp=0)

        self.plotWidget.annotate(hYMax = self.hYMax, hYMin = self.hYMin, hXMax = self.hXMax, hXMin = self.hXMin, showMean = self.showMean)

        self.layout().itemAtPosition(1,1).widget().deleteLater()
        self.layout().addWidget(self.plotWidget, 1, 1)

        try:
            self.raiseWidget(self.regLabel)
            self.raiseWidget(self.pmccLabel)
            self.raiseWidget(self.srccLabel)
        except:
            pass
        

app = QApplication(sys.argv)

data = [[1, 2, 3,  4,  5],
        [2, 7, 20, 54, 148]]

##data = [1,5,6,2,3,2,8,7,6,9,4,6,3]

m = main(data)

app.exec_()
