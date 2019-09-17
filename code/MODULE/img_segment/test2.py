import cv2
import pandas as pd
from os.path import join as pjoin


def draw_bounding_box(org, corners, color=(0, 255, 0), line=3, show=False):
    board = org.copy()
    for i in range(len(corners)):
        board = cv2.rectangle(board, (corners[i][0], corners[i][1]), (corners[i][2], corners[i][3]), color, line)
    if show:
        cv2.imshow('a', board)
        cv2.waitKey(0)
    return board


seg_path = 'E:/Mulong/Datasets/dataset_webpage/page10000/org_segment/4'
label_path = 'C:/Users/Shae/Desktop/label/merge_csv/4.csv'

label = pd.read_csv(label_path, index_col=0)

for i in range(len(label)):
    seg_no = label.iloc[i]['segment_no']

    img = cv2.imread(pjoin(seg_path, str(seg_no) + '.png'))

    cv2.imshow('img', img)
    cv2.waitKey()

