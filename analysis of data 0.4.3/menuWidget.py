from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *

import sys

from plotWidgets import *

class menuWidget(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)

        #Style dialog
        self.setStyleSheet("background-color: black; color: white; border: 0px solid black")
        
        #Set layout to vertical box layout
        self.setLayout(QVBoxLayout())
