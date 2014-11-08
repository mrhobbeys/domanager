
from setuptools import setup
import os, shutil, sys

srcPath = os.path.abspath(os.path.join("source"))
sys.path.append(srcPath)

# Remove the build folder
shutil.rmtree("build", ignore_errors=True)
shutil.rmtree("dist", ignore_errors=True)

APP = ['run.py']
DATA_FILES = [os.path.join("source", "domanager", "resources")]

OPTIONS = {'argv_emulation': True,
           'iconfile': os.path.join("source", "domanager",
                                    "resources", "main_logo_color.icns"),

           'includes': ["domanager", "sip", "PyQt5.QtCore", "PyQt5.QtWidgets", "PyQt5.QtGui"],

           "qt_plugins": ["imageformats/*", "platforms/*"],

           "excludes": ["numpy", "sqlalchemy", 'h5py', 'cx_Freeze', 'coverage',
                        'Enginio', 'PyQt5.QtBluetooth', 'PyQt5.QtHelp', 'PyQt5.QtMultimediaWidgets',
                        'PyQt5.QtPositioning', 'PyQt5.QtQml', 'PyQt5.QtQuick', 'PyQt5.QtQuickWidgets',
                        'PyQt5.QtSensors', 'PyQt5.QtSerialPort', 'PyQt5.QtWebKitWidgets', 'bs4', 'altgraph',
                        'PyQt5.QtDesigner', 'PyQt5.QtMultimedia', 'PyQt5.QtOpenGL', 'jinja2', 'email',
                        'PyQt5.QtSvg', 'PyQt5.QtSql', 'PyQt5.QtXml', 'PyQt5.QtXmlPatterns', ''
                        'PyQt5.QtWebKit', 'PyQt5.QtTest', 'PyQt5.QtScript', 'PyQt5.QtScriptTools',
                        'PyQt5.QtNetwork', 'PyQt5.QtDeclarative', 'PyQt5.QtWebSockets', 'modulegraph',
                        '_gtkagg', '_tkagg', 'bsddb', 'curses', 'pywin.debugger', 'py2app', 'mercurial'
                        'pywin.debugger.dbgcon', 'pywin.dialogs',  'tcl', 'test', 'ply', 'nose',
                        'Tkinter', 'xml', 'pywinauto.tests', 'unittest', 'Tkconstants', 'pyface',
                        'pdb', 'dummy_thread', 'doctest', 'PIL', 'PpmImagePlugin', 'traitsui',
                        'BmpImagePlugin', 'GifImagePlugin', 'GimpGradientFile', 'tornado', 'traits',
                        'GimpPaletteFile', 'JpegImagePlugin', 'PngImagePlugin', 'xlrd', 'xlwt',
                        'TiffImagePlugin', 'TiffTags', 'Image', 'ImageGrab', 'bz2'],

            'plist': {'LSUIElement': True},
            }

setup(
    name = "DO_Manager",
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
