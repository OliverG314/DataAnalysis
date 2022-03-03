from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *

import sys
from math import inf

from plotWidgets import *
from menuWidget  import *

class extrapMenu(menuWidget):
    def __init__(self, parent=None):
        menuWidget.__init__(self, parent)

        self.bigNum = 2147483647

        self.initWidgets()

    def initWidgets(self):
        #Create title label
        titleLabel = plotLabel(self, "Extrapolation")

        #Create labels showing which spinbox is minimum and which is maximum
        #Create spinboxes for minimum and maximum values to plot
        #Add them to row widgets
        
        self.minExtrapValLabel   = plotLabel(self, "Lower bound")
        self.minExtrapValSpinBox = plotSpinBox(minVal=-self.bigNum, maxVal=self.bigNum, initVal=0)

        #Set value to previously set value. If not previously set, use initial value
        self.minExtrapValSpinBox.setValue(self.parent().minExtrapVal)

        minExtrapValWidget = plotMenuRow(self, [self.minExtrapValLabel, self.minExtrapValSpinBox])

        self.maxExtrapValLabel   = plotLabel(self, "Upper bound")
        self.maxExtrapValSpinBox = plotSpinBox(minVal=-self.bigNum, maxVal=self.bigNum, initVal=0)

        #Set value to previously set value. If not previously set, use initial value
        self.maxExtrapValSpinBox.setValue(self.parent().maxExtrapVal)

        maxExtrapValWidget = plotMenuRow(self, [self.maxExtrapValLabel, self.maxExtrapValSpinBox])

        #Connect spinbox changed to procedure
        self.minExtrapValSpinBox.valueChanged.connect(self.setSpinBox)
        self.maxExtrapValSpinBox.valueChanged.connect(self.setSpinBox)

        #Add all row widgets to column layout
        for i in [titleLabel, minExtrapValWidget, maxExtrapValWidget]: self.layout().addWidget(i)

    def setSpinBox(self):
        if not (self.parent().showPolReg or self.parent().showLinReg or self.parent().showExpReg):
            return
        
        #Get values of min and max spinboxes
        minVal = self.minExtrapValSpinBox.value()
        maxVal = self.maxExtrapValSpinBox.value()

        #Plot new data based off spinbox values
        if self.sender() == self.minExtrapValSpinBox:
            self.parent().plotExtrapMin(minVal)
        elif self.sender() == self.maxExtrapValSpinBox:
            self.parent().plotExtrapMax(maxVal)

        self.activateWindow()

def excepthook(e, v, t):
    return sys.__excepthook__(e, v, t)

sys.excepthook = excepthook

if __name__ == "__main__":
    app = QApplication(sys.argv)
    e = extrapMenu()
    e.show()
    app.exec_()
