from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *

import sys

from plotWidgets import *
from menuWidget  import *

class annMenu(menuWidget):
    def __init__(self, parent=None):
        menuWidget.__init__(self, parent)

        self.initWidgets()

    def initWidgets(self):
        titleLabel = plotLabel(self, "Annotations")

        self.hYMaxCheckBox = plotCheckBox(self)
        self.hYMaxLabel    = plotLabel(self, "Highlight maximum y point(s)")

        hYMaxWidget = plotMenuRow(self, [self.hYMaxCheckBox, self.hYMaxLabel])

        self.hYMinCheckBox = plotCheckBox(self)
        self.hYMinLabel    = plotLabel(self, "Highlight minimum y point(s)")

        hYMinWidget = plotMenuRow(self, [self.hYMinCheckBox, self.hYMinLabel])

        self.hXMaxCheckBox = plotCheckBox(self)
        self.hXMaxLabel    = plotLabel(self, "Highlight maximum x point(s)")

        hXMaxWidget = plotMenuRow(self, [self.hXMaxCheckBox, self.hXMaxLabel])

        self.hXMinCheckBox = plotCheckBox(self)
        self.hXMinLabel    = plotLabel(self, "Highlight minimum x point(s)")

        hXMinWidget = plotMenuRow(self, [self.hXMinCheckBox, self.hXMinLabel])

        for i in [self.hYMaxCheckBox, self.hYMinCheckBox, self.hXMaxCheckBox, self.hXMinCheckBox]: i.setCheckState([self.parent().hYMax,
                                                                                                                    self.parent().hYMin,
                                                                                                                    self.parent().hXMax,
                                                                                                                    self.parent().hXMin][[self.hYMaxCheckBox, self.hYMinCheckBox, self.hXMaxCheckBox, self.hXMinCheckBox].index(i)])

        self.hYMaxCheckBox.stateChanged.connect(self.setCheckBox)
        self.hYMinCheckBox.stateChanged.connect(self.setCheckBox)
        self.hXMaxCheckBox.stateChanged.connect(self.setCheckBox)
        self.hXMinCheckBox.stateChanged.connect(self.setCheckBox)

        for i in [hYMaxWidget, hYMinWidget, hXMaxWidget, hXMinWidget]: self.layout().addWidget(i)

    def setCheckBox(self, state):
        self.parent().highlightMaxY(hMax = self.hYMaxCheckBox.checkState())
        self.parent().highlightMinY(hMin = self.hYMinCheckBox.checkState())
        self.parent().highlightMaxX(hMax = self.hXMaxCheckBox.checkState())
        self.parent().highlightMinX(hMin = self.hXMinCheckBox.checkState())
