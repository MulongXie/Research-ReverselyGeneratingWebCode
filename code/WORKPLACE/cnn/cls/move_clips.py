from glob import glob
import shutil
from os.path import join as pjoin
import os
from tqdm import tqdm

# src_root = 'E:\Mulong\Datasets\\rico\elements-14'
src_root = 'E:\Temp\clipping'
dest_root = 'E:\Temp\clipping_mix'

element_number = {'Button': 3000, 'Switch': 500, 'CheckBox': 500, 'RatingBar': 1000, 'Chronometer': 1000, 'TextView':20000,
                  'ImageView': 15000, 'SeekBar': 1000, 'Spinner': 1000, 'ProgressBar': 1000, 'VideoView': 1000, 'ImageButton': 6000,
                  'EditText': 1500, 'RadioButton': 1000, 'ToggleButton': 1000}
categories = [c.split('\\')[-1] for c in glob(pjoin(src_root, '*'))]

for category in categories:
    src_path = pjoin(src_root, category)
    dest_path = pjoin(dest_root, category)

    if not os.path.exists(dest_path):
        stamp = 0
        os.mkdir(dest_path)
    else:
        stamp = len(glob(pjoin(dest_path, '*.png')))

    img_files_src = glob(pjoin(src_path, '*.png'))
    # for img_file_src in tqdm(img_files_src[:element_number[category]]):
    for img_file_src in tqdm(img_files_src):
        index = stamp + int(img_file_src.split('\\')[-1].split('.')[0])
        img_file_dest = pjoin(dest_path, str(index) + '.png')
        shutil.copy(img_file_src, img_file_dest)
