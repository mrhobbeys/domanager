from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

class CustomMenu(QtGui.QMenu):
    def __init__(self, parent=None):
        super(CustomMenu, self).__init__(parent)
        self.setFocus(Qt.MouseFocusReason)
        self.setFocusPolicy(Qt.StrongFocus)