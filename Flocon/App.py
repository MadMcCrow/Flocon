# Main Window for flocon
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui


class FloconApp(QApplication):
	def __init__(self, app_name : str, parent = None):
		QApplication.__init__(self, [])
		self.window = QMainWindow()
		self.window.setWindowTitle(app_name)
		self.setApplicationDisplayName(app_name)

	def run(self, Pages) :
		for Page in Pages :
			self.window.setCentralWidget(Page)
		self.window.show()
		self.exec()
