from os.path import join as pjoin
import os
import json
import glob
import matplotlib.pyplot as plt

label_root = 'E:\Mulong\Result\web\\ui_label'
paths = glob.glob(pjoin(label_root, '*.json'))

heights = []
widths = []
ratios = []

for path in paths:
    compo_f = open(path, 'r')
    compos = json.load(compo_f)
    for compo in compos['compos']:
        if compo['class'] == 'div':
            heights.append(int(compo['height']))
            widths.append(int(compo['width']))
            ratios.append(int(compo['width']) / int(compo['height']))

p = plt.figure(1)
ax = plt.subplot(311)
ax.set_title('Shape of Block')
ax.set_xlabel('Height')
ax.set_ylabel('Number')
plt.grid(axis='y', ls='--')
plt.hist(heights, bins=50, color='#99CCFF', range=(0,1000))

ax = plt.subplot(312)
ax.set_xlabel('Width')
ax.set_ylabel('Number')
plt.grid(axis='y', ls='--')
plt.hist(widths, bins=50, color='#FFCC33', range=(0,1500))

ax = plt.subplot(313)
ax.set_xlabel('Width / Height')
ax.set_ylabel('Number')
plt.grid(axis='y', ls='--')
plt.hist(ratios, bins=50, color='#0099CC', range=(0,10))

plt.subplots_adjust(hspace=0.5)
plt.show()