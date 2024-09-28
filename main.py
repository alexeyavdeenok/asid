import sys
from interface import *
from playlist import *
from linked_list import *

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
