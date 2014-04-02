
import urllib2, os, shutil
import logging, tempfile
from PyQt4 import QtCore

from domanager.config import config

class DownloadThread(QtCore.QThread):

    progressChanged = QtCore.pyqtSignal(object)
    errorOccured = QtCore.pyqtSignal()
    downloadFinished = QtCore.pyqtSignal(object)

    def __init__(self, url, tPath, parent):
        super(DownloadThread, self).__init__(parent)
        self._fPath = tPath
        self._url = url
        self._stop = False
        self._file = None
        self._blockSize = 4096*8

    def run(self):
        try:
            u = urllib2.urlopen(self._url)
            meta = u.info()
            fileSize = int(meta.getheaders('Content-Length')[0])
            self._file = open(self._fPath, 'wb')
            downloadedBytes = 0
            while True:
                buffer = u.read(self._blockSize)
                if self._stop:
                    self._closeFile()
                    return
                elif not buffer:
                    self._closeFile()
                    tFile = self._fPath
                    self.downloadFinished.emit(tFile)
                    return
                else:
                    self._file.write(buffer)
                    downloadedBytes += self._blockSize
                    self.progressChanged.emit(float(downloadedBytes)/fileSize*100)
        except:
            self._closeFile()
            self.errorOccured.emit()
        finally:
            self._closeFile()

    def _closeFile(self):
        if self._file:
            self._file.close()

    def stopDownload(self):
        self._stop = True