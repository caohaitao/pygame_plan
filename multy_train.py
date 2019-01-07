import subprocess
import time

while True:
    p = subprocess.Popen("python plane.py",shell=True)
    p.wait()
    time.sleep(2)
    p = subprocess.Popen("python img_train.py train",shell=True)
    p.wait()