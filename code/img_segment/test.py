import cv2
import os
import pandas as pd

import segment_drawLabel as sd

root_path = "D:\datasets\dataset_webpage\data\segment"
img_root_path = os.path.join(root_path, 'img')
label_root_path = os.path.join(root_path, 'label')

name = 0
img_path = os.path.join(img_root_path, str(name))
label_path = os.path.join(label_root_path, str(name) + '\\segment.csv')
segs_img_path = os.path.join(img_path, 'segment')
labeled_img_path = os.path.join(img_path, 'labeled')

label = pd.read_csv(label_path)

print(segs_img_path)

for s in range(label.iloc[-1].segment_no + 1):

    seg_input_path = os.path.join(segs_img_path, str(s) + '.png')
    seg_output_path = os.path.join(labeled_img_path, str(s) + '.png')
    seg_img = cv2.imread(seg_input_path)
    seg_label = label[label['segment_no'] == s]
    print(seg_label)
    print(seg_output_path)

    sd.label(seg_label, seg_img, seg_output_path)
