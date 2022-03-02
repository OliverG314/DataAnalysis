from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *

import sys

from plotWidgets import *
from menuWidget  import *

class calcMenu(menuWidget):
    def __init__(self, parent=None):
        menuWidget.__init__(self, parent)

        self.initWidgets()

    def initWidgets(self):
        #Create title label
        titleLabel = plotLabel(self, "Calculations")

        #Create checkboxes to show labels containing pmcc and srcc
        #Create labels next to them
        #Set their state
        #Add them to row widgets
        
        self.pmccCheckBox = plotCheckBox(self)
        self.pmccLabel    = plotLabel(self, "PMCC")
        
        self.pmccCheckBox.setCheckState(self.parent().showPmccLabel)
        
        pmccWidget = plotMenuRow(self, [self.pmccCheckBox, self.pmccLabel])

        self.srccCheckBox = plotCheckBox(self)
        self.srccLabel    = plotLabel(self, "SRCC")

        self.srccCheckBox.setCheckState(self.parent().showSrccLabel)

        srccWidget = plotMenuRow(self, [self.srccCheckBox, self.srccLabel])

        #Connect changing of states of checkboxes to procedure
        self.pmccCheckBox.stateChanged.connect(self.setCheckBox)
        self.srccCheckBox.stateChanged.connect(self.setCheckBox)

        #Add all row widgets to column layout
        for i in [titleLabel, pmccWidget, srccWidget]: self.layout().addWidget(i)

    def setCheckBox(self, state):
        #If checkbox has been selected
        if state == Qt.Checked:
            
            #If selected checkbox was pmcc checkbox
            if self.sender() == self.pmccCheckBox:

                #Call parent procedure to show pmcc label
                self.parent().showPmcc()
            elif self.sender() == self.srccCheckBox:
                self.parent().showSrcc()

        #If checkbox has been unselected
        elif state == Qt.Unchecked:

            #If selected checkbox was srcc checkbox
            if self.sender() == self.pmccCheckBox:

                #Delete pmcc label
                self.parent().pmccLabel.deleteLater()
                self.parent().showPmccLabel = False
            elif self.sender() == self.srccCheckBox:
                self.parent().srccLabel.deleteLater()
                self.parent().showSrccLabel = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    c = calcMenu()
    c.show()
    app.exec_()
