import os
from os.path import join as pjoin
import glob
import json
import pandas as pd
import numpy as np

start_index = 0
end_index = 10000
merge_root = 'C:\\Users\\Shae\\Desktop\\label\\merge_csv'
relabel_root = 'E:\\Mulong\\Datasets\\dataset_webpage\\page10000\\relabel'
syn_root = 'C:\\Users\\Shae\\Desktop\\label\\syn'

merge_paths = glob.glob(pjoin(merge_root, '*.csv'))
merge_paths = sorted(merge_paths, key=lambda x: int(x.split('\\')[-1][:-4]))  # sorted by index

for merge_path in merge_paths:
    index = merge_path.split('\\')[-1][:-4]
    if int(index) < start_index:
        continue
    if int(index) > end_index:
        break
    relabel_path = pjoin(relabel_root, index + '.csv')
    syn_path = pjoin(syn_root, index + '.csv')
    print(merge_path)
    print(relabel_path)

    m_label = pd.read_csv(merge_path, index_col=0)
    r_label = pd.read_csv(relabel_path, index_col=0)
    syn_label = r_label.copy()

    for i in range(len(m_label)):
        compo = m_label.iloc[i]
        if compo['class'] == 'img':
            ele = {'bx': compo['column_min'], 'by':compo['row_min'], 'bw':compo['width'], 'bh':compo['height'],
                   'element':compo['class'], 'segment_no': compo['segment_no']}
            syn_label = syn_label.append(ele, ignore_index=True)

    syn_label.to_csv(syn_path)