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

    if i > 20:
        break
    i += 1
