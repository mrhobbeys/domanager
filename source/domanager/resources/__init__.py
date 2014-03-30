import os
import domanager

def rPath (fileName):
    rootDir = os.path.dirname (domanager.resources.__file__)
    filePath = os.path.join(rootDir, fileName)
    if os.path.exists(filePath):
        return filePath