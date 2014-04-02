import sys, os, shutil
from time import sleep
from subprocess import check_call, Popen, PIPE

srcPath = os.path.abspath(os.path.join("source"))
sys.path.append(srcPath)

from domanager.config import config

# Preferences
title = "DO Manager"
appName = title
sourceDir = os.path.join("dist", "%s.app" % title)
backImgDir = os.path.join("/Volumes/%s" % title, ".background")
approxSize = "70048k"
dmgPath = os.path.join("dist", "domanager.dmg")
version = config.version
finalDmgPath = os.path.join("dist", "%s_%s.dmg" % (title, version))
excludeFrameworks = ['QtMultimedia.framework', 'QtNetwork.framework', 'QtSql.framework',
                     'QtSvg.framework', 'QtXml.framework', 'QtXmlPatterns.framework',
                     'QtScript.framework', 'QtScriptTools.framework', 'QtDeclarative.framework']

# Commands
buildApp = [sys.executable, "build_pkg_mac.py",
            "py2app", "-O2", "--iconfile", "source/domanager/resources/main_logo_color.icns"]

copyBackImg = ["cp", os.path.join("source", "domanager", "resources", "back.png"), backImgDir]

createDmg = " ".join(["hdiutil", "create", "-srcfolder",
                      '"%s"' % sourceDir, "-volname", '"%s"' % title,
                      "-fs", "HFS+", "-fsargs", '"-c c=64,a=16,e=16"',
                      "-format", "UDRW", "-size", approxSize, dmgPath])

getDevice = " ".join(["hdiutil", "attach", "-readwrite", "-noverify",
                      "-noautoopen", dmgPath, "|", "egrep", "'^/dev/'", "|",
                      "sed", "1q", "|", "awk", "'{print $1}'"])

setVisualStyle = """echo '
                    tell application "Finder"
                        tell disk "'%s'"
                            open
                            set current view of container window to icon view
                            set toolbar visible of container window to false
                            set statusbar visible of container window to false
                            set the bounds of container window to {400, 100, 885, 350}
                            set theViewOptions to the icon view options of container window
                            set arrangement of theViewOptions to not arranged
                            set icon size of theViewOptions to 72
                            set background picture of theViewOptions to file ".background:'back.png'"
                            set position of item "'%s'" of container window to {100, 100}
                            make new alias file at container window to POSIX file "/Applications" with properties {name:"Applications"}
                            set position of item "Applications" of container window to {375, 100}
                            close
                            open
                            update without registering applications
                            delay 5
                            eject
                        end tell
                    end tell
                    ' | osascript""" % (title, appName)

compressRelease = """chmod -Rf go-w /Volumes/"%s"
                     sync
                     sync
                     sync
                     hdiutil detach %s
                     hdiutil convert "%s" -format UDZO -imagekey zlib-level=9 -o "%s"
                     rm -f %s"""

# Actual execution
sys.path.append(os.path.abspath("."))

check_call (buildApp)

qtConf = "; Qt Configuration file\n[Paths]\nPlugins = Resources/qt_plugins"
f = open(os.path.join(sourceDir, "Contents", "Resources", "qt.conf"), "wb")
f.write(qtConf)
f.close()

for frName in excludeFrameworks:
    frPath = os.path.join(sourceDir, "Contents", "Frameworks", frName)
    if os.path.exists(frPath):
        shutil.rmtree(frPath)

check_call (createDmg, shell=True)

result = Popen(getDevice, stdout=PIPE, shell=True)
deviceName = result.communicate()[0].replace('\n','')

sleep(5)

os.makedirs(backImgDir)
check_call (copyBackImg)

check_call (setVisualStyle, shell=True)

command = compressRelease % (title, deviceName, dmgPath, finalDmgPath, dmgPath)
check_call (command, shell=True)
