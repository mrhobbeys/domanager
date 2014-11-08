import os
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt

from domanager.config import config
from domanager.resources import rPath

class PreferencesDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(PreferencesDialog, self).__init__(parent)
        self.setWindowIcon(self._icon("settings.png"))
        self.setWindowTitle("DO Manager: Preferences")
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.setContentsMargins(5, 15, 5, 5)

        self._clientIDBox = QtWidgets.QLineEdit(self)
        clientId = config.value('clientId', "")
        self._clientIDBox.setText(clientId)
        self._clientIDBox.setMinimumWidth(250)

        self._apiKeyBox = QtWidgets.QLineEdit(self)
        self._apiKeyBox.setEchoMode(QtWidgets.QLineEdit.Password)
        apiKey = config.value('apiKey', "")
        self._apiKeyBox.setText(apiKey)
        self._apiKeyBox.setMinimumWidth(250)

        self._sshUserNameBox = QtWidgets.QLineEdit(self)
        userName = config.value('userName', "root")
        validator = QtGui.QRegExpValidator(QtCore.QRegExp("[ -~]*"), self._sshUserNameBox)
        self._sshUserNameBox.setValidator(validator)
        self._sshUserNameBox.setText(userName)
        self._sshUserNameBox.setMinimumWidth(250)

        self._sshPortBox = QtWidgets.QLineEdit(self)
        sshPort = config.value('sshPort', 22)
        validator = QtGui.QRegExpValidator(QtGui.QIntValidator(1, 65535, self._sshPortBox))
        self._sshPortBox.setValidator(validator)
        self._sshPortBox.setText("%s" % sshPort)
        self._sshPortBox.setMinimumWidth(250)

        self._formLayout = QtWidgets.QFormLayout()
        self._formLayout.setContentsMargins(5, 5, 5, 5)
        self._formLayout.addRow("Client ID: ", self._clientIDBox)
        self._formLayout.addRow("API Key: ", self._apiKeyBox)

        self._okButton = QtWidgets.QPushButton("OK")
        self._cancelButton = QtWidgets.QPushButton("Cancel")

        self._getKeysLabel = QtWidgets.QLabel(self)
        infoMsg = "<qt><a href=\"link\">Get Client ID & API Key</a></qt>"
        self._getKeysLabel.setText(infoMsg)
        self._getKeysLabel.linkActivated.connect(self._getKeys)

        self._buttonsLayout = QtWidgets.QHBoxLayout()
        self._buttonsLayout.setContentsMargins(0, 0, 0, 0)
        self._buttonsLayout.addWidget(self._getKeysLabel)
        self._buttonsLayout.addWidget(QtWidgets.QWidget(self), 1)
        self._buttonsLayout.addWidget(self._okButton)
        self._buttonsLayout.addWidget(self._cancelButton)

        self._formWidget = QtWidgets.QWidget(self)
        self._formWidget.setContentsMargins(0, 0, 0, 0)
        self._formWidget.setLayout(self._formLayout)

        self._sshLayout = QtWidgets.QFormLayout()
        self._sshLayout.setContentsMargins(5, 5, 5, 5)
        self._sshLayout.addRow("SSH User: ", self._sshUserNameBox)
        self._sshLayout.addRow("SSH Port: ", self._sshPortBox)

        self._sshWidget = QtWidgets.QWidget(self)
        self._sshWidget.setContentsMargins(0, 0, 0, 0)
        self._sshWidget.setLayout(self._sshLayout)

        self._tabs = QtWidgets.QTabWidget(self)
        self._tabs.addTab(self._formWidget, "General")
        self._tabs.addTab(self._sshWidget, "SSH")

        self._layout.addWidget(self._tabs)
        self._layout.addLayout(self._buttonsLayout)

        self._cancelButton.clicked.connect(self.close)
        self._okButton.clicked.connect(self._onOK)

        self._clientIDBox.setFocus()

    def _onOK(self):
        clientId = self._clientIDBox.text()
        apiKey = self._apiKeyBox.text()
        userName = self._sshUserNameBox.text()
        sshPort = self._sshPortBox.text()
        config.setValue('clientId', clientId)
        config.setValue('apiKey', apiKey)
        config.setValue('userName', userName)
        config.setValue('sshPort', sshPort)
        self.close()

    def _icon(self, filename):
        return QtGui.QIcon(rPath(filename))

    def _getKeys(self):
        os.system("%s https://cloud.digitalocean.com/api_access" % config.openCommand)