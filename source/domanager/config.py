
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from sys import platform

from domanager.resources import rPath

class ConfigClass(object):

    version = "0.82"

    if platform == 'win32':
        openCommand = "start"
        updateURL = 'http://www.aoizora.org/domanager/download/windows/'
        updateFileMask = 'DO_Manager_(.+?)_setup.exe'
        updateFileTempl = 'DO_Manager_%s_setup.exe'
        sshCommand = rPath('putty.exe') + " \"%s@%s:%s\""
    else:
        openCommand = "open"
        sshCommand = "osascript -e 'tell application \"Terminal\" to activate do script \"ssh -p %s %s@%s\"'"
        updateURL = 'http://www.aoizora.org/domanager/download/mac/'
        updateFileMask = 'DO_Manager_(.+?).dmg'
        updateFileTempl = 'DO_Manager_%s.dmg'

    reportUrl = 'https://github.com/itohnobue/domanager/issues/new'

    settings = QtCore.QSettings(QtCore.QSettings.NativeFormat,
                                QtCore.QSettings.UserScope,
                                "aoizora.org", "domanager")

    def value(self, name, default):
        val = self.settings.value(name, "")
        return val if val else default

    def setValue(self, name, value):
        self.settings.setValue(name, value)


config = ConfigClass()