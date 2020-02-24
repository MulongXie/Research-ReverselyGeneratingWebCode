import cv2
import numpy as np
from random import randint as rint
import time
import json


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
    :param slices: [[up, bottom], [left, right]]
    '''
    board = org.copy()
    for box in slices:
        board = cv2.rectangle(board, (box[1][0], box[0][0]), (box[1][1], box[0][1]), color, line)
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
    :param corners: [[up, bottom], [left, right]]
    '''
    if not new:
        f_in = open(file_path, 'r')
        components = json.load(f_in)
    else:
        components = {'compos': []}
    f_out = open(file_path, 'w')

    for corner in corners:
        c = {'class': 'cmopo'}
        [c['row_min'], c['row_max']], [c['column_min'], c['column_max']] = corner
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
    :param box: [up, bottom], [left, right]
    :param base_corner: [row_min, col_min]
    '''
    return [box[0][0] + base_corner[0], box[0][1] + base_corner[0]], [box[1][0] + base_corner[1], box[1][1] + base_corner[1]]


def slicing(img, leaves, base_upleft, show=False):
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
                box = [[up, bottom], [0, col]]
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
                box = [[0, row], [left, right]]
                slices.append(box)
                continue

    for box in slices:
        slice_img = img[box[0][0]:box[0][1], box[1][0]:box[1][1]]
        box = cvt_relative_box(box, base_upleft)
        children = slicing(slice_img, leaves, (box[0][0], box[1][0]), show=show)
        if len(children) == 0:
            leaves.append(box)
            if show:
                cv2.imshow('slices', slice_img)
                cv2.waitKey()
    return slices


def main():
    start = time.clock()

    org = cv2.imread('a.jpg')
    org = resize_by_height(org, resize_height=800)

    grad = gradient_laplacian(org)
    rm_noise_flood_fill(grad, show=True)
    leaves = []
    slicing(grad, leaves, (0,0), show=False)
    draw_bounding_box(org, leaves, show=True, write_path='xy.png')
    save_corners_json('xy.json', leaves)
    print(time.clock() - start)


main()