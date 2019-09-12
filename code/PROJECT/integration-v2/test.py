import matplotlib.pyplot as plt
import matplotlib

import glob
import cv2
from collections import Counter
import os
from os.path import join as pjoin

paths = glob.glob('E:\Mulong\Datasets\dataset_webpage\elements\\button\*')

heights, widths, ratios = [], [], []

for p in paths:
    img = cv2.imread(p)
    height, width = img.shape[:2]
    ratio = width / height

    heights.append(height)
    widths.append(width)
    ratios.append(ratio)

print('height:', Counter(heights))
print('width:', Counter(widths))
print('ratio:', Counter(ratios))

plt.figure(1)
plt.subplot(3,1,1).set_xlabel('Height')
plt.hist(heights,bins=60)
plt.subplot(3,1,2).set_xlabel('Width')
plt.hist(widths,bins=60)
plt.subplot(3,1,3).set_xlabel('Width / Height')
plt.hist(ratios,bins=60)
plt.show()