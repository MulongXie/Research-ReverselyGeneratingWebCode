import pytesseract as pyt
import cv2
import json
from os.path import join as pjoin, exists
from tqdm import tqdm
import multiprocessing
import numpy as np
import time

pyt.pytesseract.tesseract_cmd = 'D:\\tesseract\\tesseract\\tesseract'


def draw_bounding_box(img, bboxes, show=False, write_path=None):
    for bbox in bboxes:
        cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255,0,0), 2)
    if show:
        cv2.imshow('ocr', img)
        cv2.waitKey()
    if write_path is not None:
        cv2.imwrite(write_path, img)


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


def ocr(img, output_path=None, show=False):
    start = time.clock()
    data = pyt.image_to_data(img)
    bboxes = []
    # level|page_num|block_num|par_num|line_num|word_num|left|top|width|height|conf|text
    for d in data.split('\n')[1:]:
        d = d.split()
        conf = d[10]
        if int(conf) > 50:
            bboxes.append([int(d[6]), int(d[7]), int(d[6]) + int(d[8]), int(d[7]) + int(d[9])])
    bboxes = merge_text(bboxes)
    draw_bounding_box(img, bboxes, show=show)
    if output_path is not None:
        save_corners_json(output_path + '.json', bboxes)
    # print('OCR [%.3fs] %s' % (time.clock() - start, img_path))
    return bboxes
