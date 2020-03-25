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


def parse_results(result_file, score_threshold):
    def cvt_bbox(bbox):
        return int(bbox[0]), int(bbox[1]), int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])

    results = json.load(open(result_file, 'r'))
    compos_reform = {}
    for det in results:
        image_id = str(det['image_id'])
        score = det['score']
        if score < score_threshold:
            continue
        if image_id not in compos_reform:
            compos_reform[image_id] = {'bboxes': [cvt_bbox(det['bbox'])], 'categories':[det['category_id']]}
        else:
            compos_reform[image_id]['bboxes'].append(cvt_bbox(det['bbox']))
            compos_reform[image_id]['categories'].append(det['category_id'])
    return compos_reform


def view_results(detection, img_root, point=None):
    for i, image_id in enumerate(detection):
        print(image_id)
        if point is not None and image_id != point:
            continue
        img = cv2.imread(pjoin(img_root, image_id + '.jpg'))
        draw_bounding_box(img, detection[image_id]['bboxes'], show=True)


frcnn = parse_results('E:\Mulong\Result\\rico\\fasterrcnn.json', 0.7)
view_results(frcnn, 'E:\\Mulong\\Datasets\\rico\\combined')