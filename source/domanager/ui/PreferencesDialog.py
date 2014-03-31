import os
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from domanager.config import config
from domanager.resources import rPath

class PreferencesDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(PreferencesDialog, self).__init__(parent)
        self.setWindowIcon(self._icon("settings.png"))
        self.setWindowTitle("Preferences")

        self._layout = QtGui.QVBoxLayout(self)
        self._layout.setContentsMargins(5, 5, 5, 5)

        self._clientIDBox = QtGui.QLineEdit(self)
        clientId = config.value('clientId', "")
        self._clientIDBox.setText(clientId)
        self._clientIDBox.setMinimumWidth(250)

        self._apiKeyBox = QtGui.QLineEdit(self)
        self._apiKeyBox.setEchoMode(QtGui.QLineEdit.Password)
        apiKey = config.value('apiKey', "")
        self._apiKeyBox.setText(apiKey)
        self._apiKeyBox.setMinimumWidth(250)

        self._formlayout = QtGui.QFormLayout()
        self._formlayout.setContentsMargins(5, 5, 5, 5)
        self._formlayout.addRow("Client ID: ", self._clientIDBox)
        self._formlayout.addRow("API Key: ", self._apiKeyBox)

        self._okButton = QtGui.QPushButton("OK")
        self._cancelButton = QtGui.QPushButton("Cancel")

        self._getKeysLabel = QtGui.QLabel(self)
        infoMsg = "<qt><a href=\"link\">Get Client ID & API Key</a></qt>"
        self._getKeysLabel.setText(infoMsg)
        self._getKeysLabel.linkActivated.connect(self._getKeys)

        self._buttonsLayout = QtGui.QHBoxLayout()
        self._buttonsLayout.setContentsMargins(0, 0, 0, 0)
        self._buttonsLayout.addWidget(self._getKeysLabel)
        self._buttonsLayout.addWidget(QtGui.QWidget(self), 1)
        self._buttonsLayout.addWidget(self._okButton)
        self._buttonsLayout.addWidget(self._cancelButton)

        self._layout.addLayout(self._formlayout)
        self._layout.addLayout(self._buttonsLayout)

        self._cancelButton.clicked.connect(self.close)
        self._okButton.clicked.connect(self._onOK)

    def _onOK(self):
        config.setValue('clientId', self._clientIDBox.text())
        config.setValue('apiKey', self._apiKeyBox.text())
        self.close()

    def _icon(self, filename):
        return QtGui.QIcon(rPath(filename))

    def _getKeys(self):
        os.system("open https://cloud.digitalocean.com/api_access")