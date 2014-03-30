import sys
from PyQt4 import QtGui

from domanager.ui import TrayIcon

def start():
    app = QtGui.QApplication([])
    QtGui.QApplication.setQuitOnLastWindowClosed(False)
    doIcon = TrayIcon()
    sys.exit(app.exec_())