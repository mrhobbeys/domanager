
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
           "qt_plugins": ["imageformats/*"], }

setup(
    name = "DO Manager",
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
