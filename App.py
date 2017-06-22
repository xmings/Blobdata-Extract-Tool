import sys
from PyQt4 import QtGui
from TaskEditor import TaskEditor

app = QtGui.QApplication(sys.argv)
ex = TaskEditor()
ex.show()
sys.exit(app.exec_())	
