import os
import numpy as np

d = os.listdir('D:\datasets\PASCAL\VOCdevkit\VOC2012\JPEGImages')
d = [s.strip('.jpg') for s in d]

print(d)