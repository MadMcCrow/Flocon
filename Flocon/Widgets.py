# Widgets for Flocon

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui

#
#   Class to show a top level banner  
#
class Banner(QWidget) :
    def __init__(self, text : str, parent = None):
        QWidget.__init__(self, parent)
        self.label = QLabel(text)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.label.setFrameShape(QFrame.Box)
        self.layout.addWidget(self.label)
        self.label.setAlignment(QtCore.Qt.AlignTop)
#
#   Class to show question for the useer  
#   todo : 
#   - alignment
#   - qwhatsthis
#
class Question(QWidget):
    def __init__(self, label: str, placeholderText : str, isPassword : bool = False, parent = None):
        QWidget.__init__(self, parent)
        self.label = QLabel(label)
        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText(placeholderText)
        if isPassword:
            self.lineEdit.setEchoMode(QLineEdit.Password)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.lineEdit)

    def getInput(self):
        return self.lineEdit.text


class NavigationButtons(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

class Group(QGroupBox):
    def __init__(self, title : str, parent = None):
        QGroupBox.__init__(self, parent)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.setTitle(title)

    def addWidgets(self, widgets : list) :
        for widget in widgets:   
            self.layout.addWidget(widget)


class Page(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

    
    def addWidgets(self, widgets : list) :
        if self.layout() is None :
            self.layout = QVBoxLayout(self)
        for widget in widgets:   
            self.layout.addWidget(widget)
        self.layout.addStretch()
        self.layout.addWidget(NavigationButtons(self))
