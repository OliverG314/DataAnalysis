from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *

import sys

from plotWidgets import *
from menuWidget  import *

class extrapMenu(menuWidget):
    def __init__(self, parent=None):
        menuWidget.__init__(self, parent)

        self.initWidgets()

    def initWidgets(self):
        titleLabel = plotLabel(self, "Extrapolation")

        self.minExtrapValLabel   = plotLabel(self, "Lower bound")
        self.minExtrapValSpinBox = plotSpinBox(minVal=-250, maxVal=250, initVal=0)

        self.minExtrapValSpinBox.setValue(self.parent().minExtrapVal)

        minExtrapValWidget = plotMenuRow(self, [self.minExtrapValLabel, self.minExtrapValSpinBox])

        self.maxExtrapValLabel   = plotLabel(self, "Upper bound")
        self.maxExtrapValSpinBox = plotSpinBox(minVal=-250, maxVal=250, initVal=0)

        self.maxExtrapValSpinBox.setValue(self.parent().maxExtrapVal)

        maxExtrapValWidget = plotMenuRow(self, [self.maxExtrapValLabel, self.maxExtrapValSpinBox])

        self.minExtrapValSpinBox.valueChanged.connect(self.setSpinBox)
        self.maxExtrapValSpinBox.valueChanged.connect(self.setSpinBox)

        for i in [titleLabel, minExtrapValWidget, maxExtrapValWidget]: self.layout().addWidget(i)

    def setSpinBox(self):
        minVal = self.minExtrapValSpinBox.value()
        maxVal = self.maxExtrapValSpinBox.value()
        
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
