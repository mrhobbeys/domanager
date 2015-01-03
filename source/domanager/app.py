import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from domanager.ui import TrayIcon

def start():
    app = QtWidgets.QApplication([])
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QtWidgets.QApplication.setQuitOnLastWindowClosed(False)
    mWindow = QtWidgets.QMainWindow()
    doIcon = TrayIcon(mWindow)
    doIcon.update(True)
    sys.exit(app.exec_())