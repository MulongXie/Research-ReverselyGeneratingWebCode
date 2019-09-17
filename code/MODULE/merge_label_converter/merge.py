import json
import cv2
import numpy as np
from os.path import join as pjoin
import os

color = {'div': (0, 255, 0), 'img': (0, 0, 255), 'icon': (255, 166, 166), 'input': (255, 166, 0),
        'text': (77, 77, 255), 'search': (255, 0, 166), 'list': (166, 0, 255), 'select': (166, 166, 166),
        'button': (0, 166, 255)}


def draw_bounding_box_class(org, corners, compo_class, color_map=color, line=3, show=False, name='img'):
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


def nms(org, corners_compo_old, compos_class_old, corner_text):
    corners_compo_refine = []
    compos_class_refine = []

    corner_text = np.array(corner_text)
    for i in range(len(corners_compo_old)):
        # if compos_class_old[i] != 'img':
        #     corners_compo_refine.append(corners_compo_old[i])
        #     compos_class_refine.append(compos_class_old[i])
        #     continue

        a = corners_compo_old[i]
        noise = False
        area_a = (a[2] - a[0]) * (a[3] - a[1])
        area_text = 0
        for b in corner_text:
            area_b = (b[2] - b[0]) * (b[3] - b[1])
            # get the intersected area
            col_min_s = max(a[0], b[0])
            row_min_s = max(a[1], b[1])
            col_max_s = min(a[2], b[2])
            row_max_s = min(a[3], b[3])
            w = np.maximum(0, col_max_s - col_min_s + 1)
            h = np.maximum(0, row_max_s - row_min_s + 1)
            inter = w * h

            # calculate IoU
            ioa = inter / area_a
            iob = inter / area_b

            if compos_class_old[i] == 'img':
                # sum up all text area in a img
                if iob > 0.8:
                    area_text += area_b
                # loose threshold for img
                if ioa > 0.56:
                    noise = True
                    break
            else:
                # tight threshold for other components
                if ioa > 0.8:
                    noise = True
                    break
        # check if img is text paragraph
        if compos_class_old[i] == 'img' and area_text / area_a > 0.47:
            noise = True

        if not noise:
            corners_compo_refine.append(corners_compo_old[i])
            compos_class_refine.append(compos_class_old[i])

    return corners_compo_refine, compos_class_refine


def save_corners_json(file_path, corners, compo_classes, new=True):
    if not new:
        f_in = open(file_path, 'r')
        components = json.load(f_in)
    else:
        components = {'compos': []}
    f_out = open(file_path, 'w')

    for i in range(len(corners)):
        c = {'id': i, 'class': compo_classes[i]}
        (c['column_min'], c['row_min'], c['column_max'], c['row_max']) = corners[i]
        c['width'] = c['column_max'] - c['column_min']
        c['height'] = c['row_max'] - c['row_min']
        components['compos'].append(c)

    json.dump(components, f_out, indent=4)


def incorporate(img_path, compo_path, text_path, output_path_img, output_path_label, img_section):
    img = cv2.imread(img_path)
    img = img[:img_section[0], :img_section[1]]
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
    corners_compo_new, compos_class_new = nms(img, corners_compo, compos_class, corners_text)

    save_corners_json(output_path_label, corners_compo_new, compos_class_new, new=True)
    board = draw_bounding_box_class(img, corners_compo_new, compos_class_new)
    board = draw_bounding_box(board, corners_text, line=1)

    # cv2.imwrite(output_path_img, board)
    print('*** Merge Complete and Save to', output_path_label, '***')
