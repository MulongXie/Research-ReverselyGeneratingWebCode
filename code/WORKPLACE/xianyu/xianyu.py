import cv2
import numpy as np
from glob import glob
from os.path import join as pjoin
import json


def draw_bounding_box(org, corners, color=(0, 255, 0), line=2, show=False):
    board = org.copy()
    for i in range(len(corners)):
        board = cv2.rectangle(board, (corners[i][0], corners[i][1]), (corners[i][2], corners[i][3]), color, line)
    if show:
        cv2.imshow('a', board)
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


def read_img(img_path, resize_height):
    org = cv2.imread(img_path)
    w_h_ratio = org.shape[1] / org.shape[0]
    resize_w = resize_height * w_h_ratio
    re = cv2.resize(org, (int(resize_w), int(resize_height)))
    return re


def get_contour(org, binary):
    def cvt_bbox(bbox):
        '''
        x,y,w,h -> colmin, rowmin, colmax, rowmax
        '''
        return bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]

    board = org.copy()
    hie, contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    res_contour = []
    bboxes = []
    for i in range(len(contours)):
        if cv2.contourArea(contours[i]) < 500:
            continue
        cnt = cv2.approxPolyDP(contours[i], 0.01*cv2.arcLength(contours[i], True), True)
        res_contour.append(cnt)
        bboxes.append(cvt_bbox(cv2.boundingRect(cnt)))
    cv2.drawContours(board, res_contour, -1, (0,0,255), 1)
    draw_bounding_box(org, bboxes, (0, 255, 0), 2, show=True)
    return board


def xianyu(input_img_root='E:\\Mulong\\Datasets\\rico\\combined', show=False):
    input_paths_img = glob(pjoin(input_img_root, '*.jpg'))
    input_paths_img = sorted(input_paths_img, key=lambda x: int(x.split('\\')[-1][:-4]))  # sorted by index

    start_index = 0
    end_index = 100000
    for input_path_img in input_paths_img:
        index = input_path_img.split('\\')[-1][:-4]
        if int(index) < start_index:
            continue
        if int(index) > end_index:
            break

        org = read_img(input_path_img, 600)
        grey = cv2.cvtColor(org, cv2.COLOR_BGR2GRAY)
        equ = cv2.equalizeHist(grey)
        canny = cv2.Canny(grey, 20, 80)
        dilate = cv2.morphologyEx(canny, cv2.MORPH_DILATE, (3,3))
        contour = get_contour(org, dilate)

        if show:
            cv2.imshow('org', org)
            cv2.imshow('grey', grey)
            cv2.imshow('equ', equ)
            cv2.imshow('canny', canny)
            cv2.imshow('dilate', dilate)
            cv2.imshow('contour', contour)
            cv2.waitKey()


xianyu()
