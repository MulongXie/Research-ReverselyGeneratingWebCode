import os
import pandas as pd
import numpy as np
import shutil

data_position = 'D:\datasets\dataset_webpage\data'
root = os.path.join(data_position, 'img_relabelled')
img_root = os.path.join(root, 'img')
label_root = os.path.join(root, 'label')

i = 0
for l in os.listdir(img_root):
    shutil.copy(os.path.join(img_root, (l + '/org.png')), 'input/' + l + '.png')

    print(os.path.join(img_root, (l + '/org.png')))
    i += 1
    if i > 5:
        break
