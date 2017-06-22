# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore, Qt

class MainUI(QtGui.QWidget):
	def __init__(self, parent = None):
		super(MainUI, self).__init__(parent=None)
		self.globalLayout = QtGui.QGridLayout()
		self.setLayout(self.globalLayout)
		self.setMinimumSize(700, 500)
		self.initUI()
		
	def initUI(self):
		#工具栏
		self.newTaskButton = QtGui.QPushButton(u"新建")
		self.globalLayout.addWidget(self.newTaskButton, 0, 0, 1, 1)
		#任务表栏
		self.taskTableWidget = QtGui.QTableWidget()
		self.taskTableWidget.setColumnCount(6)
		self.taskTableWidget.setRowCount(10)
		self.taskTableWidget.horizontalHeader().setVisible(False)
		
		self.globalLayout.addWidget(self.taskTableWidget, 1, 0, 10, 4)
		
	def addTask(self, task):
		rowCount = self.taskTableWidget.rowCount()
		QtGui.QTableWidgetItem()
		
		
		
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	ex = MainUI()
	ex.show()
	#ex.alarmClock([13])
	sys.exit(app.exec_())	
		
	
	