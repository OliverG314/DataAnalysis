from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *

import sys

from plotWidgets import *
from menuWidget  import *

class hypMenu(menuWidget):
    def __init__(self, parent=None):
        menuWidget.__init__(self, parent)

        self.initWidgets()

    def initWidgets(self):
        titleLabel = plotLabel(self, "Hypotheses")

        self.pmccHypCheckBox = plotCheckBox(self)
        self.pmccHypLabel    = plotLabel(self, "PMCC hypothesis")
        pmccTails            = plotSpinBox(minVal=1, maxVal=2)

        pmccHypWidget = plotMenuRow([self.pmccHypCheckBox, self.pmccHypLabel, pmccTails])

        self.srccHypCheckBox = plotCheckBox(self)
        self.srccHypLabel    = plotLabel(self, "SRCC hypothesis")
        srccTails            = plotSpinBox(minVal=1, maxVal=2)

        srccHypWidget = plotMenuRow([self.srccHypCheckBox, self.srccHypLabel, srccTails])

        self.pmccHypCheckBox.stateChanged.connect(self.setCheckBox)
        self.srccHypCheckBox.stateChanged.connect(self.setCheckBox)

        for i in [pmccHypWidget, srccHypWidget]: self.layout().addWidget(i)

    def setCheckBox(self, state):
        if state == Qt.Checked:
            if self.sender == self.pmccHypCheckBox:
                self.parent().showPmccHyp()
            elif self.sender == self.srccHypCheckBox:
                self.parent().showSrccHyp()
