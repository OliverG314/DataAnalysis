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
        #Create title label
        titleLabel = plotLabel(self, "Annotations")

        #Create checkboxes to highlight min x, max x, min y, max y, and mean point.
        #Create labels to go next to them
        #Add them to rows of widgets

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

        self.showMeanPointCheckBox = plotCheckBox(self)
        self.showMeanPointLabel    = plotLabel(self, "Show mean point")

        showMeanPointWidget = plotMenuRow(self, [self.showMeanPointCheckBox, self.showMeanPointLabel])

        #Set states of all checkboxes to what user may have previously selected
        for i in [self.hYMaxCheckBox, self.hYMinCheckBox, self.hXMaxCheckBox, self.hXMinCheckBox, self.showMeanPointCheckBox]: i.setCheckState([self.parent().hYMax,
                                                                                                                                                self.parent().hYMin,
                                                                                                                                                self.parent().hXMax,
                                                                                                                                                self.parent().hXMin,
                                                                                                                                                self.parent().showMean][[self.hYMaxCheckBox,
                                                                                                                                                                         self.hYMinCheckBox,
                                                                                                                                                                         self.hXMaxCheckBox,
                                                                                                                                                                         self.hXMinCheckBox,
                                                                                                                                                                         self.showMeanPointCheckBox].index(i)])

        #Connect changing of states of checkboxes to procedure
        self.hYMaxCheckBox.stateChanged.connect        (self.setCheckBox)
        self.hYMinCheckBox.stateChanged.connect        (self.setCheckBox)
        self.hXMaxCheckBox.stateChanged.connect        (self.setCheckBox)
        self.hXMinCheckBox.stateChanged.connect        (self.setCheckBox)
        self.showMeanPointCheckBox.stateChanged.connect(self.setCheckBox)

        #Add all row widgets to column layout
        for i in [hYMaxWidget, hYMinWidget, hXMaxWidget, hXMinWidget, showMeanPointWidget]: self.layout().addWidget(i)

    def setCheckBox(self, state):
        #Call parent procedures based off which checkbox was selected
        self.parent().showAnnotations(hYMax     = self.hYMaxCheckBox.checkState(),
                                      hYMin     = self.hYMinCheckBox.checkState(),
                                      hXMax     = self.hXMaxCheckBox.checkState(),
                                      hXMin     = self.hXMinCheckBox.checkState(),
                                      showMean = self.showMeanPointCheckBox.checkState())

         
