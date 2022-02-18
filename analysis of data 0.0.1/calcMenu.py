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
        titleLabel = plotLabel(self, "Calculations")

        self.pmccCheckBox = plotCheckBox(self)
        self.pmccLabel    = plotLabel(self, "PMCC")

        self.pmccCheckBox.setCheckState(self.parent().showPmccLabel)

        pmccWidget = plotMenuRow(self, [self.pmccCheckBox, self.pmccLabel])

        self.srccCheckBox = plotCheckBox(self)
        self.srccLabel    = plotLabel(self, "SRCC")

        self.srccCheckBox.setCheckState(self.parent().showSrccLabel)

        srccWidget = plotMenuRow(self, [self.srccCheckBox, self.srccLabel])

        self.pmccCheckBox.stateChanged.connect(self.setCheckBox)
        self.srccCheckBox.stateChanged.connect(self.setCheckBox)

        for i in [titleLabel, pmccWidget, srccWidget]: self.layout().addWidget(i)

    def setCheckBox(self, state):
        if state == Qt.Checked:
            if self.sender() == self.pmccCheckBox:
                self.parent().showPmcc()
            elif self.sender() == self.srccCheckBox:
                self.parent().showSrcc()
        elif state == Qt.Unchecked:
            if self.sender() == self.pmccCheckBox:
                self.parent().pmccLabel.deleteLater()
                self.parent().showPmccLabel = 0
            elif self.sender() == self.srccCheckBox:
                self.parent().srccLabel.deleteLater()
                self.parent().showSrccLabel = 0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    c = calcMenu()
    c.show()
    app.exec_()
