import subprocess
import time
import pathlib
import os.path

print(pathlib.Path('../frontend').absolute())
subprocess.run(['ng build --watch'], shell=True, cwd=pathlib.Path('../frontend').absolute())
time.sleep(10)