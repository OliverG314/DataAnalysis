from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *

import sys

class plotLabel(QLabel):
    def __init__(self, parent=None, text=""):
        QLabel.__init__(self, parent)

        #Set text of label to parsed text
        self.setText(text)

        #Create font for text
        self.font = QFont("CMU Serif", 12)

        #Set font for text
        self.setFont(self.font)

        #Style label
        self.setStyleSheet("background-color: black; color: white")

        #Set width to width of text then a bit more
        self.setFixedWidth(self.fontMetrics().boundingRect(text).width()+10)

class draggablePlotLabel(plotLabel):
    def __init__(self, parent=None, text="", pos=QPoint(100, 100)):
        plotLabel.__init__(self, parent, text=text)

        #He like to move it move it
        self.move(pos)

        #Make sure label doesn't stick to mouse when released
        self.setMouseTracking(False)

    def mouseMoveEvent(self, event):
        #Get point of where label has been selected
        posPoint = QPoint(event.x() - self.geometry().width()//2,
                          event.y() - self.geometry().height()//2)

        #Move it to that point - move it to the mouse
        self.move(self.mapToGlobal(posPoint))

class plotButton(QPushButton):
    def __init__(self, parent=None, text=""):
        QPushButton.__init__(self, parent)

        #Set text of button to parsed text
        self.setText(text)

        #Create font for text
        self.font = QFont("CMU Serif", 12)

        #Set font for text
        self.setFont(self.font)

        #Style button
        self.setStyleSheet("""QPushButton {background-color: black; color: white; border: 1px solid white}
                              QPushButton:hover{background-color: rgb(25, 25, 25)}""")

class plotCheckBox(QCheckBox):
    def __init__(self, parent=None, initState=False):
        QCheckBox.__init__(self, parent)

        #Set state of checkbox to parsed state
        self.setChecked(initState)

        #Needs some stylin

class plotSpinBox(QSpinBox):
    def __init__(self, parent=None, minVal=0, maxVal=10, initVal=None):
        QSpinBox.__init__(self, parent)

        #Style spinbox
        self.setStyleSheet("background-color: black; color: white; border: 1px solid white")

        #If no default value is set, then the default value is set to the minimum
        if initVal == None:
            initVal = minVal

        #Set the range of the spinbox to go from the parsed minimum to the parsed maximum
        self.setRange(minVal, maxVal)

        #Set the default value to the parsed default value
        self.setValue(initVal)

class plotMenuRow(QWidget):
    def __init__(self, parent=None, widgets=[]):
        QWidget.__init__(self, parent)

        #Style widget
        self.setStyleSheet("background-color: black; color: white")
        
        #Set layout to horizontal box layout
        self.setLayout(QHBoxLayout())

        #Align widgets to the left
        self.layout().setAlignment(Qt.AlignLeft)

        #Loop through parsed widgets, adding them to the layout
        for i in widgets:
            self.layout().addWidget(i)

class plotDataInput(QTableWidget):
    def __init__(self, parent=None, rows=500):
        QTableWidget.__init__(self, parent)

        #Style table widget
        self.setStyleSheet("background-color: black; color: grey; border: 1px solid white")

        #Set row count to parsed number of rows
        self.setRowCount(rows)

        #Set column count to 2, as only 2 are needed: x and y
        self.setColumnCount(2)

        #Set finxed size coz it was being too small and I didn't know why
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
