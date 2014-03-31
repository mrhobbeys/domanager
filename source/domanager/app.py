import sys
from PyQt4 import QtGui

from domanager.ui import TrayIcon

def start():
    app = QtGui.QApplication([])
    QtGui.QApplication.setQuitOnLastWindowClosed(False)
    mWindow = QtGui.QMainWindow()
    doIcon = TrayIcon(mWindow)
    sys.exit(app.exec_())