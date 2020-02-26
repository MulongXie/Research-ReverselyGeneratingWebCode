import cv2
import numpy as np
from random import randint as rint
import time
import json
from os.path import join as pjoin
import multiprocessing

import xianyu_ocr as ocr
import xianyu_merge as merge


color_map = {'Text':(255,6,6), 'Non-Text':(6,255,6)}


def draw_bounding_box_class(org, corners, compo_class, line=2, show=False, name='img'):
    board = org.copy()
    for i in range(len(corners)):
        board = cv2.rectangle(board, (corners[i][0], corners[i][1]), (corners[i][2], corners[i][3]), color_map[compo_class[i]], line)
        board = cv2.putText(board, compo_class[i], (corners[i][0]+5, corners[i][1]+20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_map[compo_class[i]], 2)
    if show:
        cv2.imshow(name, board)
        cv2.waitKey(0)
    return board


def draw_region(region, board, color=None, show=False):
    if color is None:
        color = (rint(0,255), rint(0,255), rint(0,255))
    for point in region:
        board[point[0], point[1]] = color
    if show:
        cv2.imshow('region', board)
        cv2.waitKey()
    return board


def draw_bounding_box(org, slices, color=(0, 255, 0), line=2, show=False, write_path=None):
    '''
    :param slices: [[col_min, row_min, col_max, row_max]]
    '''
    board = org.copy()
    for box in slices:
        board = cv2.rectangle(board, (box[0], box[1]), (box[2], box[3]), color, line)
    if show:
        cv2.imshow('a', board)
        cv2.waitKey(0)
    if write_path is not None:
        cv2.imwrite(write_path, board)
    return board


def resize_by_height(org, resize_height):
    w_h_ratio = org.shape[1] / org.shape[0]
    resize_w = resize_height * w_h_ratio
    re = cv2.resize(org, (int(resize_w), int(resize_height)))
    return re


def save_corners_json(file_path, corners, new=True):
    '''
    :param corners: [[col_min, row_min, col_max, row_max]]
    '''
    if not new:
        f_in = open(file_path, 'r')
        components = json.load(f_in)
    else:
        components = {'compos': []}
    f_out = open(file_path, 'w')

    for corner in corners:
        c = {'category': 'Compo', 'column_min': corner[0], 'row_min': corner[1], 'column_max': corner[2], 'row_max': corner[3]}
        components['compos'].append(c)
    json.dump(components, f_out, indent=4)


def gradient_laplacian(org):
    lap = cv2.Laplacian(org, cv2.CV_16S, 3)
    lap = cv2.convertScaleAbs(lap)
    return lap


def rm_noise_flood_fill(img, grad_thresh=10, show=False):
    grad_thresh = (grad_thresh, grad_thresh, grad_thresh)
    mk = np.zeros((img.shape[0]+2, img.shape[1]+2), dtype=np.uint8)
    for x in range(0, img.shape[0], 10):
        for y in range(0, img.shape[1], 10):
            if mk[x, y] == 0:
                cv2.floodFill(img, mk, (y, x), (0,0,0), grad_thresh, grad_thresh, cv2.FLOODFILL_FIXED_RANGE)
    if show:
        cv2.imshow('floodfill', img)
        cv2.waitKey()


def cvt_relative_box(box, base_corner):
    '''
    :param box: [col_min, row_min, col_max, row_max]
    :param base_corner: [row_min, col_min]
    '''
    return [box[0] + base_corner[0], box[1] + base_corner[1], box[2] + base_corner[0], box[3] + base_corner[1]]


def slicing(img, leaves, base_upleft, show=False):
    '''
    slices: [[col_min, row_min, col_max, row_max]]
    '''
    row, col = img.shape[:2]
    slices = []
    up, bottom, left, right = -1, -1, -1, -1
    obj = False
    for x in range(row):
        if np.sum(img[x]) != 0:
            if not obj:
                up = x
                obj = True
                continue
        else:
            if obj:
                bottom = x
                obj = False
                box = [0, up, col, bottom]
                if bottom - up > 10 and (bottom - up) * col > 200:
                    slices.append(box)
                continue

    obj = False
    for y in range(col):
        if np.sum(img[:, y]) != 0:
            if not obj:
                left = y
                obj = True
                continue
        else:
            if obj:
                right = y
                obj = False
                box = [left, 0, right, row]
                if right - left > 10 and (right - left) * row > 200:
                    slices.append(box)
                continue

    for box in slices:
        slice_img = img[box[1]:box[3], box[0]:box[2]]
        box = cvt_relative_box(box, base_upleft)
        children = slicing(slice_img, leaves, (box[0], box[1]), show=show)
        if len(children) == 0:
            leaves.append(box)
            if show:
                cv2.imshow('slices', slice_img)
                cv2.waitKey()
    return slices


def detect_compo(org, output_path=None, show=False):
    start = time.clock()
    grad = gradient_laplacian(org)
    rm_noise_flood_fill(grad, show=False)
    compo_bbox = []
    slicing(grad, compo_bbox, (0, 0), show=False)
    draw_bounding_box(org, compo_bbox, show=show)
    if output_path is not None:
        save_corners_json(output_path + '.json', compo_bbox)
    # print('Compo det [%.3fs]' % (time.clock() - start))
    return compo_bbox


def xianyu(input_img_root='E:\\Mulong\\Datasets\\rico\\combined',
           output_root='E:\\Mulong\\Result\\rico\\rico_xianyu\\rico_xianyu_background',
           show=False, write_img=False):
    data = json.load(open('E:\\Mulong\\Datasets\\rico\\instances_test.json', 'r'))
    input_paths_img = [pjoin(input_img_root, img['file_name'].split('/')[-1]) for img in data['images']]
    input_paths_img = sorted(input_paths_img, key=lambda x: int(x.split('\\')[-1][:-4]))  # sorted by index

    num = 0
    start_index = 51352
    end_index = 100000
    for input_path_img in input_paths_img:
        index = input_path_img.split('\\')[-1][:-4]
        if int(index) < start_index:
            continue
        if int(index) > end_index:
            break

        start = time.clock()
        org = cv2.imread(input_path_img)
        org = resize_by_height(org, resize_height=800)

        compo = detect_compo(org, show=show)
        text = ocr.ocr(org, show=show)

        compo_all = compo + text
        categories = list(np.full(len(compo), 'Compo')) + list(np.full(len(text), 'Text'))

        print('[%.3fs] %d %s' % (time.clock() - start, num, input_path_img))


xianyu(show=True)
