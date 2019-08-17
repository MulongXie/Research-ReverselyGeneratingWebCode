from os.path import join as pjoin
import glob
import pandas as pd
import cv2
import numpy as np

import CONFIG

C = CONFIG.Config()
label_paths = glob.glob(C.ROOT_RELABEL + '/*.csv')
label_paths = sorted(label_paths, key=lambda x: int(x.split('\\')[-1][:-4]))
num = {'button':0, 'input':0}


def view(label_path, segment_path, output_root, pad=True):

    label = pd.read_csv(label_path)
    print(label)
    for i in range(len(label)):
        l = label.iloc[i]
        seg_no = str(int(l['segment_no']))
        seg_img = cv2.imread(pjoin(segment_path, seg_no + '.png'))

        print(pjoin(segment_path, seg_no + '.png'))

        x_min = int(l['bx'])
        x_max = int(l['bx']) + int(l['bw'])
        y_min = int(l['by'])
        y_max = int(l['by']) + int(l['bh'])
        element = l['element']
        num[element] += 1

        # clipping(pjoin(output_root, element, str(num[element]) + '.png'), seg_img, x_min, x_max, y_min, y_max, show=True)

        cv2.rectangle(seg_img, (x_min, y_min), (x_max, y_max), (0, 0, 255), 1)
        cv2.imshow('img', seg_img)
        cv2.waitKey(0)
    # cv2.imwrite('a.png', seg_img)

for l_path in label_paths:
    index = l_path.split('\\')[-1][:-4]
    seg_path = pjoin(C.ROOT_IMG_SEGMENT, index)

    print(l_path, seg_path)
    view(l_path, seg_path, 'component/data3')

    break