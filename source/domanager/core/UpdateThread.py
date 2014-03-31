
from time import sleep
from PyQt4 import QtCore

from domanager.core import DOHandler

class UpdateThread(QtCore.QThread):

    updated = QtCore.pyqtSignal(object)

    def __init__(self, parent):
        super(UpdateThread, self).__init__(parent)
        self._doHandler = DOHandler()

    def run(self):
        while True:
            result = self._doHandler.info()
            self.updated.emit(result)
            self.sleep(5)
