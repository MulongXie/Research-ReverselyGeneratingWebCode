import json
import numpy as np
import cv2
from glob import glob
from os.path import join as pjoin
from tqdm import tqdm


def draw_bounding_box(org, corners, color=(0, 255, 0), line=2, show=False):
    board = org.copy()
    for i in range(len(corners)):
        board = cv2.rectangle(board, (corners[i][0], corners[i][1]), (corners[i][2], corners[i][3]), color, line)
    if show:
        cv2.imshow('a', cv2.resize(board, (500, 1000)))
        cv2.waitKey(0)
    return board


def save_corners_json(file_path, corners, new=True):
    if not new:
        f_in = open(file_path, 'r')
        components = json.load(f_in)
    else:
        components = {'compos': []}
    f_out = open(file_path, 'w')

    for i in range(len(corners)):
        c = {}
        (c['column_min'], c['row_min'], c['column_max'], c['row_max']) = corners[i]
        components['compos'].append(c)
    json.dump(components, f_out, indent=4)


def load_result_multi_json(reslut_file_root):
    result_files = glob(pjoin(reslut_file_root, '*.json'))
    compos_reform = {}
    print('Loading %d detection results' % len(result_files))
    for reslut_file in tqdm(result_files):
        img_name = reslut_file.split('\\')[-1].split('_')[0]
        compos = json.load(open(reslut_file, 'r'))['compos']
        for compo in compos:
            if img_name not in compos_reform:
                compos_reform[img_name] = {'bboxes': [[compo['column_min'], compo['row_min'], compo['column_max'], compo['row_max']]]}
            else:
                compos_reform[img_name]['bboxes'].append([compo['column_min'], compo['row_min'], compo['column_max'], compo['row_max']])
    return compos_reform


def merge_text(corners, max_word_gad=40):
    def is_text_line(corner_a, corner_b):
        (col_min_a, row_min_a, col_max_a, row_max_a) = corner_a
        (col_min_b, row_min_b, col_max_b, row_max_b) = corner_b
        # on the same line
        if abs(row_min_a - row_min_b) < max_word_gad and abs(row_max_a - row_max_b) < max_word_gad:
            # close distance
            if abs(col_min_b - col_max_a) < max_word_gad or abs(col_min_a - col_max_b) < max_word_gad:
                return True
        return False

    def corner_merge_two_corners(corner_a, corner_b):
        (col_min_a, row_min_a, col_max_a, row_max_a) = corner_a
        (col_min_b, row_min_b, col_max_b, row_max_b) = corner_b

        col_min = min(col_min_a, col_min_b)
        col_max = max(col_max_a, col_max_b)
        row_min = min(row_min_a, row_min_b)
        row_max = max(row_max_a, row_max_b)
        return col_min, row_min, col_max, row_max

    changed = False
    new_corners = []
    for i in range(len(corners)):
        merged = False
        for j in range(len(new_corners)):
            if is_text_line(corners[i], new_corners[j]):
                new_corners[j] = corner_merge_two_corners(corners[i], new_corners[j])
                merged = True
                changed = True
                break
        if not merged:
            new_corners.append(corners[i])

    if not changed:
        return corners
    else:
        return merge_text(new_corners)


detect = load_result_multi_json('E:\\Mulong\\Result\\east')
for img_id in tqdm(detect):
    bboxes = merge_text(detect[img_id]['bboxes'])
    output_path = pjoin('E:\\Mulong\\Result\\east_merge', str(img_id) + '.json')
    save_corners_json(output_path, bboxes)

