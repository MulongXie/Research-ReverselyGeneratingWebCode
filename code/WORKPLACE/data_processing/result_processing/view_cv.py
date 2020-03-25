import json
from glob import glob
from os.path import join as pjoin
import cv2
import numpy as np


def draw_bounding_box(img, corners, resize_height=800, show=False, write_path=None):
    def resize_by_height(org):
        w_h_ratio = org.shape[1] / org.shape[0]
        resize_w = resize_height * w_h_ratio
        re = cv2.resize(org, (int(resize_w), int(resize_height)))
        return re

    board = img.copy()
    for corner in corners:
        board = cv2.rectangle(board, (corner[0], corner[1]), (corner[2], corner[3]), (0,255,0), thickness=3)
    board = board[100:-120]
    if show:
        cv2.imshow('all', cv2.resize(board, (500, 800)))
        cv2.waitKey(0)
    if write_path is not None:
        cv2.imwrite(write_path, board)
    return board


def resize_label(bboxes, d_height, gt_height, bias=0):
    bboxes_new = []
    scale = gt_height/d_height
    for bbox in bboxes:
        bbox = [int(b * scale + bias) for b in bbox]
        bboxes_new.append(bbox)
    return bboxes_new


def view_detect_result_json(reslut_file_root, img_file_root, show=True):
    result_files = glob(pjoin(reslut_file_root, '*.json'))
    result_files = sorted(result_files, key=lambda x: int(x.split('\\')[-1].split('.')[0]))
    print('Loading %d detection results' % len(result_files))
    for reslut_file in result_files:
        start_index = 70174
        end_index = 100000
        index = reslut_file.split('\\')[-1].split('.')[0]

        if int(index) < start_index:
            continue
        if int(index) > end_index:
            break

        org = cv2.imread(pjoin(img_file_root, index + '.jpg'))
        print(index)
        compos = json.load(open(reslut_file, 'r'))['compos']
        bboxes = []
        for compo in compos:
            print( compo['category'])
            if compo['category'] == 'Text':
                continue
            bboxes.append([compo['column_min'], compo['row_min'], compo['column_max'], compo['row_max']])
        bboxes = resize_label(bboxes, 800, org.shape[0])

        if show:
            board = draw_bounding_box(org, bboxes, show=True)
            cv2.imwrite('cv/' + str(index) + '_xianyu.png', board)


view_detect_result_json(
    # 'E:\\Mulong\\Result\\rico\\rico_uied\\rico_new_uied_cls\\merge',
    # 'E:\\Mulong\\Result\\rico\\rico_remaui\\rico_remaui_cv',
    # 'E:\\Mulong\\Result\\rico\\rico_remaui\\rico_remaui_merge',
    # 'E:\\Mulong\\Result\\rico\\rico_xianyu\\rico_xianyu_bg_cv',
    'E:\\Mulong\\Result\\rico\\rico_xianyu\\rico_xianyu_bg_ocr',
    "E:\\Mulong\\Datasets\\rico\\combined")
