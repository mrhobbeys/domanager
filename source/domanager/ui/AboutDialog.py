import os
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from domanager.resources import rPath
from domanager.config import config

class AboutDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setWindowTitle("About")
        self.setWindowIcon(self._icon("about.png"))
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self._picLabel = QtGui.QLabel(self)
        self._picLabel.setAlignment(Qt.AlignCenter)
        pmap = QtGui.QPixmap(rPath("main_logo_color.png"))
        self._picLabel.setPixmap(pmap)

        aboutTopText = "<qt>"
        aboutTopText += "<font size=5>DO Manager</font><br>"
        aboutTopText += "<b>version %s</b><br><br>" % config.version
        aboutTopText += "DigitalOcean droplets manager"
        aboutTopText += "</qt>"

        aboutBottomText = "<qt>"
        aboutBottomText += "<hr>"
        aboutBottomText += "written by <a href=\"link\">Itoh Nobue (Artur M.)</a>"
        aboutBottomText += "</qt>"

        self._aboutBoxTop = QtGui.QLabel(self)
        self._aboutBoxTop.setAlignment(Qt.AlignCenter)
        self._aboutBoxTop.setText(aboutTopText)

        self._aboutBoxBottom = QtGui.QLabel(self)
        self._aboutBoxBottom.setAlignment(Qt.AlignCenter)
        self._aboutBoxBottom.setText(aboutBottomText)
        self._aboutBoxBottom.linkActivated.connect(self._openInfo)

        self._layout = QtGui.QVBoxLayout(self)
        self._layout.addWidget(self._aboutBoxTop)
        self._layout.addWidget(self._picLabel)
        self._layout.addWidget(self._aboutBoxBottom)

    def _icon(self, filename):
        return QtGui.QIcon(rPath(filename))

    def _openInfo(self):
        os.system("open https://github.com/itohnobue")