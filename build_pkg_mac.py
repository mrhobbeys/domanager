
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
           
           "qt_plugins": ["imageformats/*"], 

           "excludes": ['PyQt4.QtDesigner', 'PyQt4.QtNetwork', 'PyQt4.QtOpenGL', 'PyQt4.QtScript', 
                        'PyQt4.QtSql', 'PyQt4.QtTest', 'PyQt4.QtWebKit', 'PyQt4.QtXml', 'PyQt4.phonon',
                        '_gtkagg', '_tkagg', 'bsddb', 'curses', 'pywin.debugger',
                        'pywin.debugger.dbgcon', 'pywin.dialogs',  'tcl', 'test', 'Tkconstants',
                        'Tkinter', 'xml', 'pywinauto.tests', 'unittest',
                        'pdb', 'dummy_thread', 'doctest', 'PIL',
                        'BmpImagePlugin', 'GifImagePlugin', 'GimpGradientFile', 
                        'GimpPaletteFile', 'JpegImagePlugin', 'PngImagePlugin', 'PpmImagePlugin', 
                        'TiffImagePlugin', 'TiffTags', 'Image', 'ImageGrab', 'bz2', 'email' ],
            }

setup(
    name = "DO Manager",
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
