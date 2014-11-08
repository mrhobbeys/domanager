import sys, os, shutil
from time import sleep
from subprocess import check_call, Popen, PIPE
from plistlib import readPlist, writePlist

srcPath = os.path.abspath(os.path.join("source"))
sys.path.append(srcPath)

from domanager.config import config

# Preferences
title = "DO_Manager"
appName = title
sourceDir = os.path.join("dist", "%s.app" % title)
approxSize = "70048k"
dmgPath = os.path.join("dist", "domanager.dmg")
pListPath = os.path.join(sourceDir, "Contents", "Info.plist")
version = config.version
finalDmgPath = os.path.join("dist", "%s_%s.dmg" % (title, version))

tempPath = os.path.join("dist", "temp")

pkgName = "Install DO Manager.pkg"
pkgPath = os.path.join(tempPath, pkgName)

# Commands
buildApp = [sys.executable, "build_pkg_mac.py",
            "py2app", "-O2", "--iconfile", "source/domanager/resources/main_logo_color.icns"]

createDmg = " ".join(["hdiutil", "create", "-srcfolder",
                      '"%s"' % tempPath, "-volname", '"%s"' % title,
                      "-fs", "HFS+", "-fsargs", '"-c c=64,a=16,e=16"',
                      "-format", "UDRW", "-size", approxSize, dmgPath])

getDevice = " ".join(["hdiutil", "attach", "-readwrite", "-noverify",
                      "-noautoopen", dmgPath, "|", "egrep", "'^/dev/'", "|",
                      "sed", "1q", "|", "awk", "'{print $1}'"])

compressRelease = """chmod -Rf go-w /Volumes/"%s"
                     sync
                     sync
                     sync
                     hdiutil detach %s
                     hdiutil convert "%s" -format UDZO -imagekey zlib-level=9 -o "%s"
                     rm -f %s"""

createAppPkg = "pkgbuild --install-location /Applications --component '%s' '%s'" % (sourceDir, pkgPath)

# Actual execution
sys.path.append(os.path.abspath("."))

print 'Building application...'
check_call(buildApp)

print 'Tweaking pList.info file...'
pList = readPlist(pListPath)
pList['NSPrincipalClass'] = 'NSApplication'
pList['NSHighResolutionCapable'] = 'True'
writePlist(pList, pListPath)

if not os.path.exists(tempPath):
    os.makedirs(tempPath)

print 'Creating PKG file...'
check_call(createAppPkg, shell=True)

print 'Creating DMG file...'
check_call(createDmg, shell=True)

result = Popen(getDevice, stdout=PIPE, shell=True)
deviceName = result.communicate()[0].replace('\n','')

sleep(5)

print 'Compressing DMG...'
command = compressRelease % (title, deviceName, dmgPath, finalDmgPath, dmgPath)
check_call(command, shell=True)

print 'Cleaning up...'
shutil.rmtree("../build", ignore_errors=True)
shutil.rmtree(tempPath, ignore_errors=True)
shutil.rmtree(sourceDir, ignore_errors=True)