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

        self.xOnYCheckBox = plotCheckBox(self)
        xOnYLabel         = plotLabel(self, "X on Y")

        self.yOnXCheckBox = plotCheckBox(self)
        yOnXLabel         = plotLabel(self, "Y on X")

        self.xOnYCheckBox.setEnabled(self.linRegCheckBox.checkState())
        self.yOnXCheckBox.setEnabled(self.linRegCheckBox.checkState())

        self.xOnYCheckBox.stateChanged.connect(self.XYRegress)
        self.yOnXCheckBox.stateChanged.connect(self.XYRegress)

        linRegWidget = plotMenuRow(self, [self.linRegCheckBox, linRegLabel, self.xOnYCheckBox, xOnYLabel, self.yOnXCheckBox, yOnXLabel])
        
        self.polRegCheckBox = plotCheckBox(self)
        polRegLabel         = plotLabel(self, "Polynomial regression")
        self.polRegSpinBox  = plotSpinBox(self, minVal=0, maxVal=25)
        polWarningLabel     = plotLabel(self, """<font color="red">WARNING: Polynomials at a high degree do weird things</font>""")

        self.polRegSpinBox.setValue(self.parent().polRegOrd)

        polRegWidget = plotMenuRow(self, [self.polRegCheckBox, polRegLabel, self.polRegSpinBox, polWarningLabel])

        self.expRegCheckBox = plotCheckBox(self)
        expRegLabel         = plotLabel(self, "Exponential regression")
        expRegWarningLabel  = plotLabel(self, """<font color="red">WARNING: It's buggy. May have to click twice</font>""")

        expRegWidget = plotMenuRow(self, [self.expRegCheckBox, expRegLabel, expRegWarningLabel])

        self.polRegSpinBox.setEnabled(False)

        self.polRegSpinBox.valueChanged.connect (lambda: self.parent().plotPolReg(order=int(self.polRegSpinBox.value())))
        self.polRegCheckBox.stateChanged.connect(lambda: self.polRegSpinBox.setEnabled(self.polRegCheckBox.checkState()))

        self.polRegCheckBox.stateChanged.connect(self.setCheckBox)
        self.linRegCheckBox.stateChanged.connect(self.setCheckBox)
        self.expRegCheckBox.stateChanged.connect(self.setCheckBox)

        for i in [self.linRegCheckBox, self.polRegCheckBox, self.expRegCheckBox]:
            i.setCheckState([self.parent().showLinReg,
                             self.parent().showPolReg,
                             self.parent().showExpReg][[self.linRegCheckBox,
                                                        self.polRegCheckBox,
                                                        self.expRegCheckBox].index(i)])

        for i in [titleLabel, polRegWidget, linRegWidget, expRegWidget]:
            self.layout().addWidget(i)

    def XYRegress(self, state):
        if state == Qt.Checked:
            if self.sender() == self.xOnYCheckBox:
                self.yOnXCheckBox.setCheckState(0)
                self.xOnYCheckBox.setCheckState(2)

                self.parent().plotLinReg("xOnY")                
            elif self.sender() == self.yOnXCheckBox:
                self.yOnXCheckBox.setCheckState(2)
                self.xOnYCheckBox.setCheckState(0)

                self.parent().plotLinReg("yOnX")

    def setCheckBox(self, state):
        self.xOnYCheckBox.setEnabled(self.linRegCheckBox.checkState())
        self.yOnXCheckBox.setEnabled(self.linRegCheckBox.checkState())
        
        if state == Qt.Checked:            
            if self.sender() == self.linRegCheckBox:
                self.linRegCheckBox.setCheckState(2)
                self.polRegCheckBox.setCheckState(0)
                self.expRegCheckBox.setCheckState(0)

                self.parent().plotLinReg()
            elif self.sender() == self.polRegCheckBox:
                self.linRegCheckBox.setCheckState(0)
                self.polRegCheckBox.setCheckState(2)
                self.expRegCheckBox.setCheckState(0)

                self.parent().plotPolReg(order=int(self.polRegSpinBox.value()))
            elif self.sender() == self.expRegCheckBox:
                self.linRegCheckBox.setCheckState(0)
                self.polRegCheckBox.setCheckState(0)
                self.expRegCheckBox.setCheckState(2)

                self.parent().plotExpReg()
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
