import sys, os

os.environ['PYTHONIOENCODING'] = 'utf-8'
srcPath = os.path.abspath(os.path.join("source"))
sys.path.append(srcPath)
sys.path.append(".")

from domanager import app
app.start()