from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt

class CustomMenu(QtWidgets.QMenu):
    def __init__(self, parent=None):
        super(CustomMenu, self).__init__(parent)
        self.setFocus(Qt.MouseFocusReason)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)

        self._checkTimer = QtCore.QTimer(self)
        self._checkTimer.timeout.connect(self._checkMouse)

        self._closeTimer = QtCore.QTimer(self)
        self._closeTimer.timeout.connect(self.close)

    def _checkMouse(self):
        if not self.underMouse() and not self._closeTimer.isActive():
            self._closeTimer.start(5000)

    def closeEvent(self, e):
        self._checkTimer.stop()
        super(CustomMenu, self).closeEvent(e)

    def mouseMoveEvent(self, e):
        self._closeTimer.stop()
        if not self._checkTimer.isActive():
            self._checkTimer.start(100)
        super(CustomMenu, self).mouseMoveEvent(e)