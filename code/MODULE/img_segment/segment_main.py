import cv2
import numpy as np
import os
import pandas as pd

import segment_utils as seg

root_path = "E:\Mulong\Datasets\dataset_webpage\page10000"
img_root_path = os.path.join(root_path, 'org')
label_root_path = os.path.join(root_path, 'label')

name = 1

# segment the image and corresponding label
segment_size = 600
seg.segment_img(segment_size, name, img_root_path)
seg.segment_label(segment_size, name, label_root_path)

# draw labels on segments
seg.segment_draw_label_by_no(img_root_path, label_root_path, name)