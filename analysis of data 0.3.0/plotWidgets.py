from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *

import sys

class plotLabel(QLabel):
    def __init__(self, parent=None, text=""):
        QLabel.__init__(self, parent)

        self.setText(text)
        
        self.font = QFont("CMU Serif", 12)
        
        self.setFont(self.font)

        self.setStyleSheet("background-color: black; color: white")

        text = text.replace("<sup>", " ")
        text = text.replace("</sup>", " ")

        self.setFixedWidth(self.fontMetrics().boundingRect(text).width()+10)

#parentVar parameter will be changed in later update
#Future update will initialise one label for each time it's needed, (pmccLabel, srccLabel, etc.), and hide/show it when needed
class draggablePlotLabel(plotLabel):
    def __init__(self, parent=None, text="", pos=QPoint(100, 100)):
        plotLabel.__init__(self, parent, text=text)

        self.move(pos)

        self.setMouseTracking(False)

    def mouseMoveEvent(self, event):
        posPoint = QPoint(event.x() - self.geometry().width()//2,
                          event.y() - self.geometry().height()//2)
        
        self.move(self.mapToGlobal(posPoint))

class plotButton(QPushButton):
    def __init__(self, parent=None, text=""):
        QPushButton.__init__(self, parent)

        self.text = text

        self.setText(text)

        self.font = QFont("CMU Serif", 12)

        self.setFont(self.font)

        self.setStyleSheet("""QPushButton {background-color: black; color: white; border: 1px solid white}
                              QPushButton:hover{background-color: rgb(25, 25, 25)}""")

class plotCheckBox(QCheckBox):
    def __init__(self, parent=None, initState=False):
        QCheckBox.__init__(self, parent)

        self.setChecked(initState)

class plotSpinBox(QSpinBox):
    def __init__(self, parent=None, minVal=0, maxVal=10, initVal=None):
        QSpinBox.__init__(self, parent)

        self.setStyleSheet("background-color: black; color: white; border: 1px solid white")

        if initVal == None:
            initVal = minVal

        self.setRange(minVal, maxVal)
        self.setValue(initVal)

class plotMenuRow(QWidget):
    def __init__(self, parent=None, widgets=[]):
        QWidget.__init__(self, parent)

        self.setLayout(QHBoxLayout())
        self.setStyleSheet("background-color: black; color: white")

        self.layout().setAlignment(Qt.AlignLeft)

        for i in widgets:
            self.layout().addWidget(i)

class plotDataInput(QTableWidget):
    def __init__(self, parent=None, rows=500):
        QTableWidget.__init__(self, parent)

        self.setStyleSheet("background-color: black; color: grey; border: 1px solid white")

        self.setRowCount(rows)
        self.setColumnCount(2)

        self.setFixedSize(255, 250)

def excepthook(e, v, t):
    return sys.__excepthook__(e, v, t)

sys.excepthook = excepthook

if __name__ == "__main__":
    app = QApplication(sys.argv)
    p = QTableWidget(20, 20)
    p.show()
    print(p.item(1,1))
    app.exec_()
