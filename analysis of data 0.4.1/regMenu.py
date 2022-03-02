from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *

import sys

from plotWidgets import *
from menuWidget  import *

class regMenu(menuWidget):
    def __init__(self, parent=None):
        menuWidget.__init__(self, parent)
        
        self.initWidgets()

    def initWidgets(self):
        #Create title label
        titleLabel = plotLabel(self, "Regressions")

        #Create checkboxes for which regression should be displayed
        #Create labels to go next to them
        #Add them to rows of widgets
        
        self.polRegCheckBox = plotCheckBox(self)
        polRegLabel         = plotLabel(self, "Polynomial regression")

        #Create spin box for order of polynomial
        self.polRegSpinBox = plotSpinBox(self, minVal=0, maxVal=25)

        #Create warning label coz warning
        polWarningLabel = plotLabel(self, """<font color="red">WARNING: Polynomials at a high degree do weird things</font>""")

        #Set value to value that user may have previously selected
        self.polRegSpinBox.setValue(self.parent().polRegOrd)

        polRegWidget = plotMenuRow(self, [self.polRegCheckBox, polRegLabel, self.polRegSpinBox, polWarningLabel])

        self.linRegCheckBox = plotCheckBox(self)
        linRegLabel         = plotLabel(self, "Linear regression")

        self.xOnYCheckBox = plotCheckBox(self)
        xOnYLabel         = plotLabel(self, "X on Y")

        self.yOnXCheckBox = plotCheckBox(self)
        yOnXLabel         = plotLabel(self, "Y on X")

        #If linear regression has been selected then allow for the choice of x on y, or y on x
        self.xOnYCheckBox.setEnabled(self.linRegCheckBox.checkState())
        self.yOnXCheckBox.setEnabled(self.linRegCheckBox.checkState())

        #Set states of linear regression modes to what user may have previously selected
        self.xOnYCheckBox.setCheckState(self.parent().xOnY)
        self.yOnXCheckBox.setCheckState(self.parent().yOnX)

        #Connect changing of states of linear regression modes to to procedure
        self.xOnYCheckBox.stateChanged.connect(self.XYRegress)
        self.yOnXCheckBox.stateChanged.connect(self.XYRegress)

        linRegWidget = plotMenuRow(self, [self.linRegCheckBox, linRegLabel, self.xOnYCheckBox, xOnYLabel, self.yOnXCheckBox, yOnXLabel])

        self.expRegCheckBox = plotCheckBox(self)
        expRegLabel         = plotLabel(self, "Exponential regression")

        #Ye this is buggy too
        expRegWarningLabel  = plotLabel(self, """<font color="red">WARNING: It's buggy. May have to click twice</font>""")

        expRegWidget = plotMenuRow(self, [self.expRegCheckBox, expRegLabel, expRegWarningLabel])

        #If polynomial regression has been selected then allow for the choice of order of polynomial
        self.polRegSpinBox.setEnabled(self.polRegCheckBox.checkState())

        #Connect spinbox value changed to plotting polynomial regression with new order
        self.polRegSpinBox.valueChanged.connect(lambda: self.parent().plotPolReg(order=int(self.polRegSpinBox.value())))

        #Connect changing of state of polynomial regression checkbox to enabling of order spinbox
        self.polRegCheckBox.stateChanged.connect(lambda: self.polRegSpinBox.setEnabled(self.polRegCheckBox.checkState()))

        #Connect changing of states of any of the regression checkboxes to procedure
        self.polRegCheckBox.stateChanged.connect(self.setCheckBox)
        self.linRegCheckBox.stateChanged.connect(self.setCheckBox)
        self.expRegCheckBox.stateChanged.connect(self.setCheckBox)

        #Set states of all checkboxes to what user may have previously selected
        for i in [self.linRegCheckBox, self.polRegCheckBox, self.expRegCheckBox]:
            i.setCheckState([self.parent().showLinReg,
                             self.parent().showPolReg,
                             self.parent().showExpReg][[self.linRegCheckBox,
                                                        self.polRegCheckBox,
                                                        self.expRegCheckBox].index(i)])

        #Add all row widgets to column layout
        for i in [titleLabel, polRegWidget, linRegWidget, expRegWidget]: self.layout().addWidget(i)

    #Procedure for regressing x on y/y on x
    def XYRegress(self, state):
        if state == Qt.Checked:

            #If x on y checkbox selected
            if self.sender() == self.xOnYCheckBox:

                #Turn off y on x checkbox
                self.yOnXCheckBox.setCheckState(0)
                self.xOnYCheckBox.setCheckState(2)

                #Plot regression accordingly
                self.parent().plotLinReg("xOnY")                
            elif self.sender() == self.yOnXCheckBox:
                self.yOnXCheckBox.setCheckState(2)
                self.xOnYCheckBox.setCheckState(0)

                self.parent().plotLinReg("yOnX")

    def setCheckBox(self, state):
        #Disbale x on y/y on x checboxes if necessary
        self.xOnYCheckBox.setEnabled(self.linRegCheckBox.checkState())
        self.yOnXCheckBox.setEnabled(self.linRegCheckBox.checkState())
        
        if state == Qt.Checked:
            
            #If linear regression selected
            if self.sender() == self.linRegCheckBox:

                #Turn off exponential and polynomial regressions
                self.linRegCheckBox.setCheckState(2)
                self.polRegCheckBox.setCheckState(0)
                self.expRegCheckBox.setCheckState(0)

                #Plot linear regression based on whether x on y/y on x has been selected
                self.parent().plotLinReg(["xOnY", "yOnX"][[self.xOnYCheckBox.checkState(), self.yOnXCheckBox.checkState()].index(2)])
            elif self.sender() == self.polRegCheckBox:
                self.linRegCheckBox.setCheckState(0)
                self.polRegCheckBox.setCheckState(2)
                self.expRegCheckBox.setCheckState(0)

                #Plot polynomial regression and parse order of polynomial
                self.parent().plotPolReg(order=int(self.polRegSpinBox.value()))
            elif self.sender() == self.expRegCheckBox:
                self.linRegCheckBox.setCheckState(0)
                self.polRegCheckBox.setCheckState(0)
                self.expRegCheckBox.setCheckState(2)

                self.parent().plotExpReg()
        else:

            #Clear plot
            self.parent().clearLines()

def excepthook(e, v, t):
    return sys.__excepthook__(e, v, t)

sys.excepthook = excepthook

if __name__ == "__main__":
    app = QApplication(sys.argv)
    r = regMenu(None)
    r.show()
    app.exec_()
