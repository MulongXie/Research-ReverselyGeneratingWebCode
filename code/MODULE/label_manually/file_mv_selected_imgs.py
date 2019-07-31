import pandas as pd
import glob
from os.path import join as pjoin
from shutil import copy
import os


def move_selected_img(img_root='E:\\Mulong\\Datasets\\dataset_webpage\\img_segment', label_root='E:\\Mulong\\Datasets\\dataset_webpage\\relabel'):
    new_root = pjoin(img_root.replace('img_segment', 'img_segment_selected'))
    label_paths = glob.glob(pjoin(label_root, '*.csv'))
    label_paths.sort(key=lambda x: int(x.split('\\')[-1][:-4]))

    for label_path in label_paths:
        index = label_path.split('\\')[-1][:-4]
        label = pd.read_csv(label_path)
        pre_seg_no = -1
        for i in range(len(label)):
            l = label.iloc[i]
            seg_no = l['segment_no']
            if seg_no == pre_seg_no:
                continue
            else:
                pre_seg_no = seg_no
            old_path = pjoin(img_root, index, str(int(seg_no)) + '.png')
            new_path = pjoin(new_root, index)
            if not os.path.exists(new_path):
                os.mkdir(new_path)
            new_path = pjoin(new_path, str(int(seg_no)) + '.png')
            copy(old_path, new_path)

move_selected_img()