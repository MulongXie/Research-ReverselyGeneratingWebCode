import os
import shutil
from CONFIG import Config

C = Config()
input_root = C.IMG_ROOT
output_root = C.OUTPUT_ROOT

data_position = 'D:\datasets\dataset_webpage\data'
root = os.path.join(data_position, 'img_relabelled')
img_root = os.path.join(root, 'img')
label_root = os.path.join(root, 'label')

i = 0
for l in os.listdir(img_root):
    shutil.copy(os.path.join(img_root, (l + '/org.png')), os.path.join(input_root, (l + '.png')))
