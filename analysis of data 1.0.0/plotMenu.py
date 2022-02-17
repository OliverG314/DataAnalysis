from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *

import sys

from plotWidgets import *
from regMenu     import *
from calcMenu    import *

class plotMenu(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setStyleSheet("background-color: black; color: white")
        self.setLayout(QVBoxLayout())

        self.layout().setAlignment(Qt.AlignTop)
        self.layout().setSpacing(25)

        self.initWidgets()

    def initWidgets(self):
        for i in range(len(self.window().menuText)):
            menuButton = plotButton(self, text=self.window().menuText[i])

            menuButton.clicked.connect(lambda clicked, menu=self.window().menus[i]: self.window().showMenu(menu))

            self.layout().addWidget(menuButton)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    p = plotMenu()
    p.show()
    app.exec_()
