from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt

class CustomMenu(QtWidgets.QMenu):
    def __init__(self, parent=None):
        super(CustomMenu, self).__init__(parent)
        self.setFocus(Qt.MouseFocusReason)
        self.setFocusPolicy(Qt.StrongFocus)