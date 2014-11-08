from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt

from domanager.resources import rPath
from domanager.config import config

class DownloadDialog(QtWidgets.QDialog):

    cancelDownload = QtCore.pyqtSignal()

    def __init__(self, version, parent=None):
        super(DownloadDialog, self).__init__(parent)
        self._layout = QtWidgets.QVBoxLayout(self)
        msg = "Downloading update (%s)..." % version
        self._layout.addWidget(QtWidgets.QLabel(msg))
        self.setWindowTitle("DO Manager: Update")
        self.setWindowIcon(self._icon('update.png'))

        self._pg = QtWidgets.QProgressBar(self)
        self._pg.setAlignment(Qt.AlignCenter)
        self._layout.addWidget(self._pg)

        self._bCancel = QtWidgets.QPushButton("Cancel")
        self._bCancel.clicked.connect(self._onCancel)

        self._bLayout = QtWidgets.QHBoxLayout()
        self._bLayout.addWidget(QtWidgets.QWidget(self), 1)
        self._bLayout.addWidget(self._bCancel)
        self._bLayout.setContentsMargins(0, 0, 0, 0)

        self._layout.addLayout(self._bLayout)

        self.resize(350, 10)

        sg = QtWidgets.QApplication.desktop().screenGeometry()
        self.move(sg.center() - self.rect().center())

    def _onCancel(self):
        self.cancelDownload.emit()

    def setProgress(self, value):
        if value > 100:
            value = 100
        self._pg.setValue(value)
        QtWidgets.QApplication.processEvents()


    def _icon(self, filename):
        return QtGui.QIcon(rPath(filename))