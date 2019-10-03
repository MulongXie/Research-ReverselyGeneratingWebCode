import cv2
import glob
from os.path import join as pjoin
import matplotlib.pyplot as plt

root_button = 'E:\Mulong\Datasets\dataset_webpage\Components2\\button'
root_input = 'E:\Mulong\Datasets\dataset_webpage\Components2\\input'
root_img = 'E:\Mulong\Datasets\dataset_webpage\Components2\\img'

paths = glob.glob(pjoin(root_img, '*'))

heights = []
widths = []
ratios = []

for i, path in enumerate(paths):
    img = cv2.imread(path)
    try:
        heights.append(img.shape[0])
        widths.append(img.shape[1])
        ratios.append(img.shape[1] / img.shape[0])
    except:
        continue

    # if i > 20000:
    #     break

p = plt.figure(1)
ax = plt.subplot(311)
ax.set_title('Shape of Image')
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