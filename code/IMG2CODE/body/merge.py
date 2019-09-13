import json
import cv2
import numpy as np
from os.path import join as pjoin
import os

from CONFIG import Config
C = Config()
compo_index = {'img':0, 'text':0, 'button':0, 'input':0, 'icon':0}


def draw_bounding_box_class(org, corners, compo_class, color_map=C.COLOR, line=3, show=False, name='img'):
    board = org.copy()
    for i in range(len(corners)):
        if compo_class[i] == 'text':
            continue
        board = cv2.rectangle(board, (corners[i][0], corners[i][1]), (corners[i][2], corners[i][3]), color_map[compo_class[i]], line)
        board = cv2.putText(board, compo_class[i], (corners[i][0]+5, corners[i][1]+20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_map[compo_class[i]], 2)
    if show:
        cv2.imshow(name, board)
        cv2.waitKey(0)
    return board


def draw_bounding_box(org, corners, color=(0, 255, 0), line=3, show=False):
    board = org.copy()
    for i in range(len(corners)):
        board = cv2.rectangle(board, (corners[i][0], corners[i][1]), (corners[i][2], corners[i][3]), color, line)
    if show:
        cv2.imshow('a', board)
        cv2.waitKey(0)
    return board


def save_clipping(org, corners, compo_classes, compo_index, output_root=C.ROOT_IMG_COMPONENT):
    if output_root is None:
        output_root = C.ROOT_IMG_COMPONENT
    if not os.path.exists(output_root):
        os.mkdir(output_root)
    pad = 1
    for i in range(len(corners)):
        compo = compo_classes[i]
        (col_min, row_min, col_max, row_max) = corners[i]
        col_min = max(col_min - pad, 0)
        col_max = min(col_max + pad, org.shape[1])
        row_min = max(row_min - pad, 0)
        row_max = min(row_max + pad, org.shape[0])

        # if component type already exists, index increase by 1, otherwise add this type
        compo_path = pjoin(output_root, compo)
        if not os.path.exists(compo_path):
            os.mkdir(compo_path)
        if compo_classes[i] not in compo_index:
            compo_index[compo_classes[i]] = 0
        else:
            compo_index[compo_classes[i]] += 1
        clip = org[row_min:row_max, col_min:col_max]
        cv2.imwrite(pjoin(compo_path, str(compo_index[compo_classes[i]]) + '.png'), clip)


def nms(corners_compo_old, compos_class_old, corner_text):
    corners_compo_refine = []
    compos_class_refine = []

    corner_text = np.array(corner_text)
    for i in range(len(corners_compo_old)):
        if compos_class_old[i] != 'img':
            corners_compo_refine.append(corners_compo_old[i])
            compos_class_refine.append(compos_class_old[i])
            continue

        a = corners_compo_old[i]
        noise = False
        area_a = (a[2] - a[0]) * (a[3] - a[1])
        for b in corner_text:
            # get the intersected area
            col_min_s = max(a[0], b[0])
            row_min_s = max(a[1], b[1])
            col_max_s = min(a[2], b[2])
            row_max_s = min(a[3], b[3])
            w = np.maximum(0, col_max_s - col_min_s + 1)
            h = np.maximum(0, row_max_s - row_min_s + 1)
            inter = w * h

            # calculate IoU
            iou = inter / area_a

            if iou > 0.2:
                noise = True
                break
        if not noise:
            corners_compo_refine.append(corners_compo_old[i])
            compos_class_refine.append(compos_class_old[i])

    return corners_compo_refine, compos_class_refine


def incorporate(img_path, compo_path, text_path, output_path, is_clip=False, clip_path=None):
    img = cv2.imread(img_path)
    compo_f = open(compo_path, 'r')
    text_f = open(text_path, 'r')

    compos = json.load(compo_f)
    corners_compo = []
    compos_class = []
    corners_text = []
    for compo in compos['compos']:
        corners_compo.append([compo['column_min'], compo['row_min'], compo['column_max'], compo['row_max']])
        compos_class.append(compo['class'])
    for line in text_f.readlines():
        if len(line) > 1:
            corners_text.append([int(c) for c in line[:-1].split(',')])

    corners_compo_new, compos_class_new = nms(corners_compo, compos_class, corners_text)

    board = draw_bounding_box_class(img, corners_compo_new, compos_class_new)
    board = draw_bounding_box(board, corners_text, line=1)

    cv2.imwrite(output_path, board)

    if is_clip:
        save_clipping(img, corners_compo_new, compos_class_new, compo_index, clip_path)
