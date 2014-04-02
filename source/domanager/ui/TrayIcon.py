import sys, os, subprocess, gc
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from domanager.config import config
from domanager.resources import rPath
from domanager.core import DOHandler, UpdateThread
from domanager.ui.PreferencesDialog import PreferencesDialog
from domanager.ui.AboutDialog import AboutDialog
from domanager.ui.RenameDialog import RenameDialog

class TrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, mWindow):
        super(TrayIcon, self).__init__(mWindow)
        self.setIcon(self._icon("main_logo_gray.png"))
        self.setVisible(True)

        self._mainWindow = mWindow
        self._mainWindow.setWindowIcon(self._icon("main_logo_color.png"))

        self._doHandler = DOHandler()

        self._data = []
        self._dInfos = []
        self._menu = None

        self._quitAction = QtGui.QAction("Quit", self)
        self._quitAction.setIcon(self._icon("quit.png"))
        self._quitAction.triggered.connect(self._quit)

        self._aboutAction = QtGui.QAction("About", self)
        self._aboutAction.setIcon(self._icon("about.png"))
        self._aboutAction.triggered.connect(self._about)

        self._settingsAction = QtGui.QAction("Preferences", self)
        self._settingsAction.setIcon(self._icon("settings.png"))
        self._settingsAction.triggered.connect(self._settings)

        self._createAction = QtGui.QAction("Create droplet (web)", self)
        self._createAction.setIcon(self._icon("create.png"))
        self._createAction.triggered.connect(self._createDroplet)

        self._bugAction = QtGui.QAction("Report bug/request", self)
        self._bugAction.setIcon(self._icon("bug.png"))

        self._updateAction = QtGui.QAction("Check for update", self)
        self._updateAction.setIcon(self._icon("update.png"))

        self._helpMenu = QtGui.QMenu(self._mainWindow)
        self._helpMenu.addAction(self._updateAction)
        self._helpMenu.addAction(self._bugAction)
        self._helpMenu.addAction(self._aboutAction)

        self._helpAction = QtGui.QAction("Help", self)
        self._helpAction.setIcon(self._icon("help.png"))
        self._helpAction.setMenu(self._helpMenu)

        self._updateThread = UpdateThread(self)
        self._updateThread.updated.connect(self._updateData)
        self._updateThread.start()

        clientId = config.value('clientId', "")
        apiKey = config.value('apiKey', "")

        if not clientId or not apiKey:
            self._settings()

        self._updateMenu()

    def _icon(self, filename):
        return QtGui.QIcon(rPath(filename))

    def _dropletMenu(self, idx):
        dropletMenu = QtGui.QMenu(self._mainWindow)

        copyIPAction = QtGui.QAction("Copy IP to clipboard", dropletMenu)
        copyIPAction.setIcon(self._icon("ip.png"))
        copyIPAction.triggered.connect(lambda y, x=idx: self._ipToClipboard(x))

        resetRootAction = QtGui.QAction("Reset root password", dropletMenu)
        resetRootAction.setIcon(self._icon("password.png"))
        resetRootAction.triggered.connect(lambda y, x=idx: self._resetRoot(x))

        renameDropletAction = QtGui.QAction("Rename", dropletMenu)
        renameDropletAction.setIcon(self._icon("rename.png"))
        renameDropletAction.triggered.connect(lambda y, x=idx: self._renameDroplet(x))

        destroyDropletAction = QtGui.QAction("Destroy", dropletMenu)
        destroyDropletAction.setIcon(self._icon("destroy.png"))
        destroyDropletAction.triggered.connect(lambda y, x=idx: self._destroyDroplet(x))

        dropletMenu.addAction(copyIPAction)

        if self._dInfos[idx]['status'] == 'active':

            sshAction = QtGui.QAction("Open SSH connection", dropletMenu)
            sshAction.setIcon(self._icon("ssh.png"))
            sshAction.triggered.connect(lambda y, x=idx: self._openSSH(x))

            rebootAction = QtGui.QAction("Power cycle", dropletMenu)
            rebootAction.setIcon(self._icon("reboot.png"))
            rebootAction.triggered.connect(lambda y, x=idx: self._powerCycle(x))

            shutDownAction = QtGui.QAction("Power Off", dropletMenu)
            shutDownAction.setIcon(self._icon("shutdown.png"))
            shutDownAction.triggered.connect(lambda y, x=idx: self._powerOff(x))

            dropletMenu.addAction(sshAction)
            dropletMenu.addSeparator()
            dropletMenu.addAction(renameDropletAction)
            dropletMenu.addAction(resetRootAction)
            dropletMenu.addAction(rebootAction)
            dropletMenu.addAction(shutDownAction)

        else:
            startAction = QtGui.QAction("Power On", dropletMenu)
            startAction.setIcon(self._icon("start.png"))
            startAction.triggered.connect(lambda y, x=idx: self._powerOn(x))

            dropletMenu.addSeparator()
            dropletMenu.addAction(renameDropletAction)
            dropletMenu.addAction(resetRootAction)
            dropletMenu.addAction(startAction)

        dropletMenu.addSeparator()
        dropletMenu.addAction(destroyDropletAction)

        return dropletMenu

    def _checkResult(self, commandName, dropletName, result):
        if result['status'] == 'OK':
            msg = "%s command to %s was sent successfully" % (commandName, dropletName)
            self._message(msg)
        else:
            if 'pending' in result['message']:
                msg = "%s is in pending stage. Please try again later" % dropletName
            else:
                msg = result['message']
            self._message(msg, error=True)

    def _renameDroplet(self, idx):
        dropletName = self._dInfos[idx]['name']
        dropletId = self._dInfos[idx]['id']
        rd = RenameDialog(dropletName, self._mainWindow)
        rd.showNormal()
        rd.activateWindow()
        rd.exec_()
        if rd.result:
            result = self._doHandler.rename(dropletId, rd.result)
            self._checkResult("Rename", dropletName, result)

    def _resetRoot(self, idx):
        dropletName = self._dInfos[idx]['name']
        action = "reboot" if self._dInfos[idx]['status'] == 'active' else "power on"
        result = self._question("Reset root password command will %s the %s. Proceed?" % (action, dropletName))
        if result:
            dropletId = self._dInfos[idx]['id']
            result = self._doHandler.resetRoot(dropletId)
            self._checkResult("Reset root", dropletName, result)

    def _openSSH(self, idx):
        userName = config.value('userName', "root")
        ipAddress = self._dInfos[idx]['ip_address']
        command = config.sshCommand
        command = command % (userName, ipAddress)
        os.system(command)

    def _powerOn(self, idx):
        dropletName = self._dInfos[idx]['name']
        dropletId = self._dInfos[idx]['id']
        result = self._doHandler.powerOn(dropletId)
        self._checkResult("Power on", dropletName, result)

    def _powerCycle(self, idx):
        dropletName = self._dInfos[idx]['name']
        result = self._question("Are you sure that you want to power cycle the %s?" % dropletName)
        if result:
            dropletId = self._dInfos[idx]['id']
            result = self._doHandler.powerCycle(dropletId)
            self._checkResult("Power cycle", dropletName, result)

    def _destroyDroplet(self, idx):
        dropletName = self._dInfos[idx]['name']
        result = self._question("Are you sure that you want to DESTROY the %s? This command is irreversible!" % dropletName)
        if result:
            dropletName = self._dInfos[idx]['name']
            dropletId = self._dInfos[idx]['id']
            result = self._doHandler.destroy(dropletId)
            self._checkResult("Destroy", dropletName, result)

    def _powerOff(self, idx):
        dropletName = self._dInfos[idx]['name']
        result = self._question("Are you sure that you want to power off the %s?" % dropletName)
        if result:
            dropletName = self._dInfos[idx]['name']
            dropletId = self._dInfos[idx]['id']
            result = self._doHandler.powerOff(dropletId)
            self._checkResult("Power off", dropletName, result)

    def _updateData(self, result):
        if self._data != result:
            self._dInfos = []
            self._data = result
            if 'droplets' in self._data:
                self._dInfos = self._data['droplets']
            self._updateMenu()

    def _updateMenu(self):
        menuVisible = False
        if self._menu:
            menuVisible = self._menu.isVisible()
            self._menu.hide()

        self._menu = QtGui.QMenu(self._mainWindow)

        if not self._data:
            infoMsg = "Connecting..."
            self.setIcon(self._icon("main_logo_gray.png"))
        elif "OK" in self._data['status']:
            infoMsg = "Connected"
            self.setIcon(self._icon("main_logo_gray.png"))
        elif "ERROR" in self._data['status']:
            infoMsg = self._data['message']
            self.setIcon(self._icon("main_logo_gray_error.png"))
        else:
            infoMsg = self._data['status']
            self.setIcon(self._icon("main_logo_gray_error.png"))

        infoAction = QtGui.QAction("  Status: %s" % infoMsg, self._menu)
        infoAction.setEnabled(False)

        self._menu.addAction(infoAction)
        self._menu.addSeparator()

        if len(self._dInfos) > 0:
            for idx, dInfo in enumerate(self._dInfos):
                dropletAction = QtGui.QAction(dInfo['name'], self._menu)

                if dInfo['status'] == 'active':
                    if dInfo['locked']:
                        dropletAction.setIcon(self._icon("locked.png"))
                        dropletAction.setToolTip("Locked (operation in progress)")
                    else:
                        dropletAction.setIcon(self._icon("active.png"))
                        dropletAction.setToolTip("Running")
                else:
                    dropletAction.setIcon(self._icon("inactive.png"))
                    dropletAction.setToolTip("Stopped")

                if not dInfo['locked']:
                    dropletAction.setMenu(self._dropletMenu(idx))

                self._menu.addAction(dropletAction)

            self._menu.addSeparator()

        self._menu.addAction(self._createAction)
        self._menu.addSeparator()
        self._menu.addAction(self._settingsAction)
        self._menu.addAction(self._helpAction)
        self._menu.addSeparator()
        self._menu.addAction(self._quitAction)

        self.activated.connect(self._popupMenu)
        if menuVisible:
            self._popupMenu()

    def _popupMenu(self):
        rect = self.geometry()
        self._menu.popup(QtCore.QPoint(rect.x(), rect.y()))

    def _ipToClipboard(self, idx):
        ipAddress = self._dInfos[idx]['ip_address']
        clipboard = QtGui.QApplication.clipboard()
        mimeData = QtCore.QMimeData()
        mimeData.setText(ipAddress)
        clipboard.setMimeData(mimeData)
        QtGui.QApplication.processEvents()

    def __messageBox(self, msg, mIcon):
        mBox = QtGui.QMessageBox(self._mainWindow)
        mBox.setWindowTitle("DO Manager")
        mBox.setText(msg)
        mBox.setWindowFlags(mBox.windowFlags() | Qt.WindowStaysOnTopHint)
        mBox.setIcon(mIcon)
        return mBox

    def _message(self, msg, error=False):
        mIcon = QtGui.QMessageBox.Warning if error else QtGui.QMessageBox.Information
        mBox = self.__messageBox(msg, mIcon)
        mBox.exec_()

    def _question(self, msg):
        mBox = self.__messageBox(msg, QtGui.QMessageBox.Question)
        mBox.setStandardButtons(mBox.Yes | mBox.No)
        return mBox.exec_() == mBox.Yes

    def _createDroplet(self):
        os.system("%s https://cloud.digitalocean.com/droplets/new" % config.openCommand)

    def _settings(self):
        pd = PreferencesDialog(self._mainWindow)
        pd.showNormal()
        pd.activateWindow()
        pd.exec_()

    def _about(self):
        ad = AboutDialog(self._mainWindow)
        ad.showNormal()
        ad.activateWindow()
        ad.exec_()

    def _quit(self):
        sys.exit(0)