import sys
from PyQt5 import QtWidgets

from domanager.ui import TrayIcon

def start():
    app = QtWidgets.QApplication([])
    QtWidgets.QApplication.setQuitOnLastWindowClosed(False)
    mWindow = QtWidgets.QMainWindow()
    doIcon = TrayIcon(mWindow)
    doIcon.update(True)
    sys.exit(app.exec_())