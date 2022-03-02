from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *

import sys

from plotWidgets import *
from menuWidget  import *

class dataMenu(menuWidget):
    def __init__(self, parent=None):
        menuWidget.__init__(self, parent)

        #Copy data
        self.dataCopy = self.parent().data.copy()

        #Number of rows in spreadsheet for data input
        self.rows = 1000

        self.initWidgets()

    def initWidgets(self):
        #Create title label
        titleLabel = plotLabel(self, "Data")

        #Create widget for data input
        self.dataInputWidget = plotDataInput(self, rows=self.rows)

        #Create buttons to plot data, clear data, or cancel data input
        pltButton    = plotButton(self, "Plot data")
        clearButton  = plotButton(self, "Clear")
        cancelButton = plotButton(self, "Cancel")

        #Add buttons to row widget
        okClearCancelWidget = plotMenuRow(self, [pltButton, clearButton, cancelButton])

        #Connect button clicks to procedures
        pltButton.clicked.connect   (self.plotData)
        clearButton.clicked.connect (self.clearData)
        cancelButton.clicked.connect(self.cancelData)

        #Set data in spreadsheet to currently plotted data
        for x in range(2):
            for y in range(len(self.parent().data[1])):
                self.dataInputWidget.setItem(y, x, QTableWidgetItem(str(self.parent().data[x][y])))

        #Add all row widgets to column layout
        for i in [titleLabel, self.dataInputWidget, okClearCancelWidget]: self.layout().addWidget(i)

    #Procedure to plot inputted data
    def plotData(self):
        #Create list to store data
        dataList = []
        
        for x in range(2):
            dataList.append([])
            
            for y in range(self.rows):
                try:
                    
                    #Append numbers in spreadsheet to 2d list
                    dataList[x].append(int(self.dataInputWidget.item(y, x).text()))
                except Exception as e:

                    #If the data sets aren't equal in length, the invalid data will be brutally obliterated
                    break

        #Plot new data                
        self.parent().initUI(dataList)

        #Commit suicide
        self.deleteLater()

    #Procedure to clear all data
    def clearData(self):
        for x in range(2):
            for y in range(self.rows):
                try:
                    #Set all cells in spreadsheet to be empty
                    self.dataInputWidget.item(y, x).setText("")
                except:
                    break

    #Procedure to revert all inputs
    def cancelData(self):

        #Plot previous data
        self.parent().initUI(self.dataCopy)

        #Commit suicide
        self.deleteLater()
