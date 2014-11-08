
import urllib2, re, os, subprocess
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt

from domanager.resources import rPath
from domanager.config import config
from domanager.ui.DownloadDialog import DownloadDialog
from domanager.core import DownloadThread

class UpdateChecker(QtCore.QObject):

    quitProgram = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(UpdateChecker, self).__init__(parent)
        self._dDialog = None
        self._dThread = None
        self._fName = None

    def _icon(self, filename):
        return QtGui.QIcon(rPath(filename))

    def __messageBox(self, msg, mIcon):
        mBox = QtWidgets.QMessageBox(self.parent())
        mBox.setWindowTitle("DO Manager")
        mBox.setText(msg)
        mBox.setWindowFlags(mBox.windowFlags() | Qt.WindowStaysOnTopHint)
        mBox.setIcon(mIcon)
        return mBox

    def _dialog(self, msg, question=False):
        if question:
            mBox = self.__messageBox(msg, QtWidgets.QMessageBox.Question)
            mBox.setStandardButtons(mBox.Yes | mBox.No)
            return mBox.exec_() == mBox.Yes
        else:
            mBox = self.__messageBox(msg, QtWidgets.QMessageBox.Information)
            mBox.exec_()

    def _onError(self):
        self._closeDialog()
        msg = "There was an error while downloading your update.\n"
        msg += "Please try again later."
        self._dialog(msg)

    def check(self):
        if self._dDialog:
            self._dDialog.activateWindow()
            self._dDialog.showNormal()
        else:
            try:
                response = urllib2.urlopen(config.updateURL)
                info = response.info()
                content = info.dict['content-disposition']
                m = re.search(config.updateFileMask, content)
                if m:
                    newVersion = m.group(1)
                    if newVersion > config.version:
                        msg = "New version (%s) is availabale. Do you want to download it now?\n" % newVersion
                        if self._dialog(msg, question=True):
                            self._fName = config.updateFileTempl % newVersion
                            self._fName = os.path.join(os.path.expanduser("~/Downloads"), self._fName)
                            self._download(config.updateURL, self._fName, newVersion)
                    else:
                        self._dialog('Your version is up-to-date (%s)' % config.version)
                else:
                    self._dialog('Your version is up-to-date (%s)' % config.version)
            except:
                self._dialog("Can't connect to update server")

    def _download(self, url, fName, version):
        self._dDialog = DownloadDialog(version, self.parent())
        self._dThread = DownloadThread(url, fName, self.parent())
        self._dThread.progressChanged.connect(self._dDialog.setProgress)
        self._dThread.errorOccured.connect(self._onError)
        self._dThread.downloadFinished.connect(self._onFinished)
        self._dDialog.cancelDownload.connect(self._onCancel)
        self._dDialog.showNormal()
        self._dThread.start()

    def _onFinished(self, fPath):
        self._closeDialog()
        if os.path.isfile(fPath):
            try:
                subprocess.call(["%s" % config.openCommand, fPath])
                self.quitProgram.emit()
            except:
                self._onError()

    def _onCancel(self):
        self._dThread.stopDownload()
        self._closeDialog()
        if os.path.isfile(self._fName):
            try:
                os.remove(self._fName)
            except:
                pass

    def _closeDialog(self):
        if self._dDialog:
            self._dDialog.close()
        self._dDialog = None