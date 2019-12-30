#!python3
# Run all the programs (doctests and demos) in the current folder.

import glob, importlib, os, sys

for file in glob.iglob("*.py"):
    if "run_all_tests" in file:
        continue
    print("\n\nProcessing "+file)
    command = '"'+sys.executable+'"'+" "+file+" quiet"
    os.system(command)
