
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

class ConfigClass(object):

    version = "0.81"

    sshCommand = "osascript -e 'tell application \"Terminal\" to activate do script \"ssh -p %s %s@%s\"'"
    openCommand = "open"

    reportUrl = 'https://github.com/itohnobue/domanager/issues/new'

    updateURL = 'http://www.aoizora.org/domanager/download/mac/'
    updateFileMask = 'DO Manager_(.+?).dmg'
    updateFileTempl = 'DO Manager_%s.dmg'

    settings = QtCore.QSettings(QtCore.QSettings.NativeFormat,
                                QtCore.QSettings.UserScope,
                                "aoizora.org", "domanager")

    def value(self, name, default):
        val = self.settings.value(name, "")
        return val if val else default

    def setValue(self, name, value):
        self.settings.setValue(name, value)


config = ConfigClass()