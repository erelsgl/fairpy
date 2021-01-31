import os, sys
print("file path is ", os.path.realpath(__file__))
print("os.cwd is ", os.getcwd())
print("PYTHONPATH is ", os.environ['PYTHONPATH'])
print("sys.path is ", sys.path)
