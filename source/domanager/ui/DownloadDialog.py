from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from domanager.resources import rPath
from domanager.config import config

class DownloadDialog(QtGui.QDialog):

    cancelDownload = QtCore.pyqtSignal()

    def __init__(self, version, parent=None):
        super(DownloadDialog, self).__init__(parent)
        self._layout = QtGui.QVBoxLayout(self)
        msg = "Downloading update (%s)..." % version
        self._layout.addWidget(QtGui.QLabel(msg))
        self.setWindowTitle("DO Manager: Update")
        self.setWindowIcon(self._icon('update.png'))

        self._pg = QtGui.QProgressBar(self)
        self._pg.setAlignment(Qt.AlignCenter)
        self._layout.addWidget(self._pg)

        self._bCancel = QtGui.QPushButton("Cancel")
        self._bCancel.clicked.connect(self._onCancel)

        self._bLayout = QtGui.QHBoxLayout()
        self._bLayout.addWidget(QtGui.QWidget(self), 1)
        self._bLayout.addWidget(self._bCancel)
        self._bLayout.setContentsMargins(0, 0, 0, 0)

        self._layout.addLayout(self._bLayout)

        self.resize(350, 10)

        sg = QtGui.QApplication.desktop().screenGeometry()
        self.move(sg.center() - self.rect().center())

    def _onCancel(self):
        self.cancelDownload.emit()

    def setProgress(self, value):
        if value > 100:
            value = 100
        self._pg.setValue(value)
        QtGui.QApplication.processEvents()


    def _icon(self, filename):
        return QtGui.QIcon(rPath(filename))