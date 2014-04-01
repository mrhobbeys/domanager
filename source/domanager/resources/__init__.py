import os
import domanager

def rPath(fileName):
    rootDir = domanager.resources.__path__[0]
    filePath = os.path.join(rootDir, fileName)
    if os.path.exists(filePath):
        return filePath
    else:
        frPath = os.path.join ("resources", fileName)
        if os.path.exists(frPath):
            return frPath
