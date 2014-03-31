
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

class ConfigClass(object):

    version = "1.0"

    settings = QtCore.QSettings(QtCore.QSettings.NativeFormat,
                                QtCore.QSettings.UserScope,
                                "aoizora.org", "domanager")

    def value(self, name, default):
        val = self.settings.value(name, "")
        return val if val else default

    def setValue(self, name, value):
        self.settings.setValue(name, value)


config = ConfigClass()