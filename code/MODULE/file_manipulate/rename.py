import cv2
import glob
import os
from os.path import join as pjoin
import numpy as np

g = glob.glob('C:\\Users\Shae\Desktop\\text\*')

root = '\\'.join(g[0].split('\\')[:-1])
for i in range(len(g)):

    # img = cv2.imread(g[i])
    # if img.shape[0] > 35 and img.shape[1] > 35:
    #     os.remove(g[i])

    os.renames(g[i], pjoin(root, str(i) + 'a.png'))

print(len(g))