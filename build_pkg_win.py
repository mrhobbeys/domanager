import os, shutil, logging
import psutil
import enchant
import smtplib, email
from distutils.dir_util import copy_tree

from cx_Freeze import setup, Executable

distDir = "dist"

# Remove the build folder
shutil.rmtree("build", ignore_errors=True)
shutil.rmtree("dist", ignore_errors=True)

try:
    os.mkdir(os.path.abspath(distDir))
except:
    logging.exception('')

folders_to_copy = [os.path.join('source', 'domanager', 'resources')]
for f in folders_to_copy:
    fPath = os.path.join(distDir, os.path.basename(f))
    copy_tree(f, fPath)

pluginsDir = "C:\Python27_x32\lib\site-packages\PyQt4\plugins\imageformats"
copy_tree(os.path.abspath(pluginsDir), os.path.join(distDir, 'imageformats'))

GUI2Exe_Target_1 =  Executable(
        script                = "run.py",
        targetName            = "domanager.exe",
        icon                  = os.path.join("source", "domanager", "resources", "main_logo_color.ico"),
        base                  = 'Win32GUI',
        targetDir             = "dist",
        initScript            = None,
        compress              = True,
        copyDependentFiles    = True,
        appendScriptToExe     = False,
        appendScriptToLibrary = False,
)

setup(
    name        = "DO Manager",
    version     = "1.0",
    author      = "Aoizora Org",
    description = "DO Manager",
    options     = {
        "build_exe": {
            "packages": [
                'PyQt4.QtCore',
                'PyQt4.QtGui',
                'sip'
            ],
            "excludes": [
                'PyQt4.QtDesigner', 'PyQt4.QtNetwork', 'PyQt4.QtOpenGL', 'PyQt4.QtScript',
                'PyQt4.QtSql', 'PyQt4.QtTest', 'PyQt4.QtWebKit', 'PyQt4.QtXml', 'PyQt4.phonon',
                '_gtkagg', '_tkagg', 'bsddb', 'curses', 'pywin.debugger',
                'pywin.debugger.dbgcon', 'pywin.dialogs', 'QtMultimedia',
                'QtNetwork', 'QtNetwork4', 'QtWebKit', 'tcl', 'test', 'Tkconstants',
                'Tkinter', 'xml', 'pywinauto.tests', 'unittest',
                'pdb', 'dummy_thread', 'doctest', 'PIL',
                'QtXml', 'BmpImagePlugin', 'GifImagePlugin', 'GimpGradientFile',
                'GimpPaletteFile', 'JpegImagePlugin', 'PngImagePlugin', 'PpmImagePlugin',
                'TiffImagePlugin', 'TiffTags', 'Image', 'ImageGrab', 'bz2'
            ],
            "path":          [],
            "includes":      ['PyQt4', 'sip'],
            "include_files": [],
        }
    },
    executables = [GUI2Exe_Target_1]
)