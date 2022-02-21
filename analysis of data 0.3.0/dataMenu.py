from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *

import sys

from plotWidgets import *
from menuWidget  import *

class dataMenu(menuWidget):
    def __init__(self, parent=None):
        menuWidget.__init__(self, parent)

        self.dataCopy = self.parent().data.copy()

        self.rows = 1000

        self.initWidgets()

    def initWidgets(self):
        titleLabel = plotLabel(self, "Data")

        self.dataInputWidget = plotDataInput(self, rows=self.rows)

        okButton     = plotButton(self, "Plot data")
        clearButton  = plotButton(self, "Clear")
        cancelButton = plotButton(self, "Cancel")

        okCancelWidget = plotMenuRow(self, [okButton, clearButton, cancelButton])

        okButton.clicked.connect(self.plotData)
        clearButton.clicked.connect(self.clearData)
        cancelButton.clicked.connect(self.cancelData)

        for x in range(2):
            for y in range(len(self.parent().data[1])):
                self.dataInputWidget.setItem(y, x, QTableWidgetItem(str(self.parent().data[x][y])))

        for i in [titleLabel, self.dataInputWidget, okCancelWidget]: self.layout().addWidget(i)

    def plotData(self):
        dataList = []
        for x in range(2):
            dataList.append([])
            for y in range(self.rows):
                try:
                    dataList[x].append(int(self.dataInputWidget.item(y, x).text()))
                except Exception as e:
                    break
                
        self.parent().initUI(dataList)

        self.deleteLater()

    def clearData(self):
        for x in range(2):
            for y in range(self.rows):
                try:
                    self.dataInputWidget.item(y, x).setText("")
                except:
                    break

##        self.plotData()
##        self.deleteLater()

    def cancelData(self):
        self.parent().initUI(self.dataCopy)

        self.deleteLater()
