import cv2
import numpy as np
import os


def segment_img(org, segment_size, output_path, overlap=100):
    height, width = np.shape(org)[0], np.shape(org)[1]
    print(np.shape(org))

    top = 0
    bottom = segment_size
    segment_no = 0
    while top < height and bottom < height:
        segment = org[top:bottom]
        cv2.imwrite(os.path.join(output_path, str(segment_no) + '.png'), segment)
        segment_no += 1
        top += segment_size - overlap
        bottom = bottom + segment_size - overlap if bottom + segment_size - overlap <= height else height
