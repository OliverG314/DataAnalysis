from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *

import sys

from plotWidgets import *
from menuWidget  import *

class regMenu(menuWidget):
    def __init__(self, parent=None):
        menuWidget.__init__(self, parent)

        self.layout().setAlignment(Qt.AlignLeft)
        
        self.initWidgets()

    def initWidgets(self):
        titleLabel = plotLabel(self, "Regressions")

        self.linRegCheckBox = plotCheckBox(self)
        linRegLabel         = plotLabel(self, "Linear regression")

        linRegWidget = plotMenuRow(self, [self.linRegCheckBox, linRegLabel])
        
        self.polRegCheckBox = plotCheckBox(self)
        polRegLabel         = plotLabel(self, "Polynomial regression")
        self.polRegSpinBox  = plotSpinBox(self, minVal=0, maxVal=25)
        polWarningLabel     = plotLabel(self, """<font color="red">WARNING: Polynomials at a high degree do weird things</font>""")

        self.polRegSpinBox.setValue(self.parent().polRegOrd)

        polRegWidget = plotMenuRow(self, [self.polRegCheckBox, polRegLabel, self.polRegSpinBox, polWarningLabel])

        self.polRegSpinBox.setEnabled(False)

        self.polRegSpinBox.valueChanged.connect(lambda: self.parent().plotPolReg(order=int(self.polRegSpinBox.value())))

        self.polRegCheckBox.stateChanged.connect(lambda: self.polRegSpinBox.setEnabled(self.polRegCheckBox.checkState()))
        self.polRegCheckBox.stateChanged.connect(self.setCheckBox)
        
        self.linRegCheckBox.stateChanged.connect(self.setCheckBox)

        for i in [self.linRegCheckBox, self.polRegCheckBox]: i.setCheckState([self.parent().showLinReg, self.parent().showPolReg][[self.linRegCheckBox, self.polRegCheckBox].index(i)])

        for i in [titleLabel, polRegWidget, linRegWidget]: self.layout().addWidget(i)

    def setCheckBox(self, state):
        if state == Qt.Checked:
            if self.sender() == self.linRegCheckBox:
                self.linRegCheckBox.setCheckState(2)
                self.polRegCheckBox.setCheckState(0)

                self.parent().plotLinReg()
            elif self.sender() == self.polRegCheckBox:
                self.linRegCheckBox.setCheckState(0)
                self.polRegCheckBox.setCheckState(2)

                self.parent().plotPolReg(order=int(self.polRegSpinBox.value()))

        else:
            self.parent().clearLines()

def excepthook(e, v, t):
    return sys.__excepthook__(e, v, t)

sys.excepthook = excepthook

if __name__ == "__main__":
    app = QApplication(sys.argv)
    r = regMenu(None)
    r.show()
    app.exec_()
