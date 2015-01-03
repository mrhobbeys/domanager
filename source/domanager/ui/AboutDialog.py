import os
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt

from domanager.resources import rPath
from domanager.config import config

class AboutDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setWindowTitle("About DO Manager")
        self.setWindowIcon(self._icon("about.png"))
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self._picLabel = QtWidgets.QLabel(self)
        self._picLabel.setAlignment(Qt.AlignCenter)
        pmap = QtGui.QPixmap(rPath("main_logo_color.png"))
        pmap = pmap.scaledToHeight(256, Qt.SmoothTransformation)
        pmap.setDevicePixelRatio(2)
        self._picLabel.setPixmap(pmap)

        aboutTopText = "<qt>"
        aboutTopText += "<font size=5>DO Manager</font><br>"
        aboutTopText += "<b>version %s</b><br><br>" % config.version
        aboutTopText += "DigitalOcean droplets manager"
        aboutTopText += "</qt>"

        aboutBottomText = "<qt>"
        aboutBottomText += "<hr>"
        aboutBottomText += "made by <a href=\"link\">Itoh Nobue (Artur M.)</a>"
        aboutBottomText += "</qt>"

        self._aboutBoxTop = QtWidgets.QLabel(self)
        self._aboutBoxTop.setAlignment(Qt.AlignCenter)
        self._aboutBoxTop.setText(aboutTopText)

        self._aboutBoxBottom = QtWidgets.QLabel(self)
        self._aboutBoxBottom.setAlignment(Qt.AlignCenter)
        self._aboutBoxBottom.setText(aboutBottomText)
        self._aboutBoxBottom.linkActivated.connect(self._openInfo)

        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.addWidget(self._aboutBoxTop)
        self._layout.addWidget(self._picLabel)
        self._layout.addWidget(self._aboutBoxBottom)

    def _icon(self, filename):
        return QtGui.QIcon(rPath(filename))

    def _openInfo(self):
        self.close()
        os.system("%s https://github.com/itohnobue" % config.openCommand)
