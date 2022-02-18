from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *

import sys

class dataInputWidget(QTableWidget):
    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)

        self.setStyleSheet("background-color: black; color: grey")

        self.rows = 2
        self.cols = 100

        self.setRowCount(self.rows)
        self.setColumnCount(self.cols)

        self.setFixedHeight(102)

        self.setParentData()

        self.cellChanged.connect(self.updateData)

    def setParentData(self):
        data = self.window().data

        for i in range(self.cols):
            try:
                if not data[0][i] != None: self.setItem(0, i, QTableWidgetItem(data[0][i]))
            except:
                pass

        for i in range(self.cols):
            try:
                if not data[1][i] != None: self.setItem(1, i, QTabelWidgetItem(data[1][i]))
            except:
                pass
    
    def updateData(self):
        data = [[],[]]
        for i in range(self.cols):
            try:    data[0].append(int(self.item(0, i).text()))
            except: break

            try:    data[1].append(int(self.item(1, i).text()))
            except: break  

        self.window().initUI(data)

def excepthook(e, v, t):
    return sys.__excepthook__(e, v, t)

sys.excepthook = excepthook

if __name__ == "__main__":
    app = QApplication(sys.argv)
    d = dataInputWidget()
    d.show()
    app.exec_()
