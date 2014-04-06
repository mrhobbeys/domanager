# -*- coding: utf-8 -*-
import time, sys, os, shutil, codecs, uuid, re, glob

from os import environ
from subprocess import check_call

srcPath = os.path.abspath(os.path.join("source"))
sys.path.append(srcPath)
sys.path.append(".")

def replaceStringInFile(filePath, searchString, replaceString):
    file = codecs.open(filePath, "r", "utf-8")
    data = file.read()
    file.close()

    file = codecs.open(filePath, "w", "utf-8")
    file.write( re.sub(searchString, replaceString, data)  )
    file.close()

def readVersion():
    try:
        from domanager.config import config
        return config.version
    except:
        print "Could not read config.version variable from vgp.config"
        raise
        sys.exit(1)

if len(sys.argv) > 2:
    print "Usage: python build_win.py"
    sys.exit(1)
else:
    versionNum = readVersion()

    check_call(["python", "build_pkg_win.py", "build_exe"])

    for filename in glob.glob(os.path.join("build", "exe.win32-2.7", '*.*')):
        if os.path.isfile(filename):
            shutil.copy(filename, "dist")

    shutil.copyfile("vcredist_2008_x86.exe", os.path.join("dist", "vcredist_2008_x86.exe"))

    outFileName = "DO_Manager_" + versionNum + "_setup.exe"
    shutil.copyfile("domanager.nsi", "domanager_patched.nsi")

    replaceStringInFile("domanager_patched.nsi", "APP_NAME",     "DO Manager")
    replaceStringInFile("domanager_patched.nsi", "VERSION_NAME",  versionNum)
    replaceStringInFile("domanager_patched.nsi", "DIST_DIR",     "dist")
    replaceStringInFile("domanager_patched.nsi", "OUT_FILE_NAME", outFileName)

    check_call(["makensis.exe", "domanager_patched.nsi"])

    if os.path.isfile("domanager_patched.nsi"):
        os.remove( "domanager_patched.nsi" )

    shutil.rmtree("build", ignore_errors=True)
    shutil.rmtree("dist",  ignore_errors=True)