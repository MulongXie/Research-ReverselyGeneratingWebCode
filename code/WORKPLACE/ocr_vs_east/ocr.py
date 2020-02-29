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
        cv2.imshow('ocr', cv2.resize(img, (int(img.shape[1]/3), int(img.shape[0]/3))))
        cv2.waitKey()
    if write_path is not None:
        cv2.imwrite(write_path, cv2.resize(img, (int(img.shape[1]), int(img.shape[0]))))


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


def ocr(img_path, output_path, num, show=True):
    start = time.clock()
    img = cv2.imread(img_path)
    data = pyt.image_to_data(img)
    bboxes = []
    # level|page_num|block_num|par_num|line_num|word_num|left|top|width|height|conf|text
    for d in data.split('\n')[1:]:
        d = d.split()
        conf = d[10]
        if int(conf) != -1:
            bboxes.append([int(d[6]), int(d[7]), int(d[6]) + int(d[8]), int(d[7]) + int(d[9])])
    bboxes = merge_text(bboxes)
    save_corners_json(output_path + '.json', bboxes)
    draw_bounding_box(img, bboxes, show=show, write_path=None)
    print('%d [%.3fs] %s' % (num, time.clock() - start, img_path))


root_input = "E:\\Mulong\\Datasets\\rico\\combined"
root_output = 'E:\\Mulong\\Result\\ocr'
data = json.load(open('E:\\Mulong\\Datasets\\rico\\instances_test.json', 'r'))
input_paths_img = [pjoin(root_input, img['file_name'].split('/')[-1]) for img in data['images']]
input_paths_img = sorted(input_paths_img, key=lambda x: int(x.split('\\')[-1][:-4]))  # sorted by index

if __name__ == '__main__':
    # concurrently running on multiple processors
    cpu_num = 1
    pool = multiprocessing.Pool(processes=cpu_num)
    # set the range of target inputs' indices
    num = 0
    start_index = 872
    end_index = 100000
    for input_path_img in input_paths_img:
        index = input_path_img.split('\\')[-1][:-4]
        if int(index) < start_index:
            continue
        if int(index) > end_index:
            break
        output_path = pjoin(root_output, index)
        # *** start processing ***
        pool.apply_async(ocr, (input_path_img, output_path, num, ))
        num += 1
    pool.close()
    pool.join()