from os.path import join as pjoin
import os
import glob
import pandas as pd
import cv2
import numpy as np
import json
from tqdm import tqdm

element_map = {'0':'Button', '1':'CheckBox', '2':'Chronometer', '3':'EditText', '4':'ImageButton', '5':'ImageView',
               '6':'ProgressBar', '7':'RadioButton', '8':'RatingBar', '9':'SeekBar', '10':'Spinner', '11':'Switch',
               '12':'ToggleButton', '13':'VideoView', '14':'TextView'}
element_number = {'Button': 0, 'Switch': 0, 'CheckBox': 0, 'RatingBar': 0, 'Chronometer': 0, 'TextView':0,
                  'ImageView': 0, 'SeekBar': 0, 'Spinner': 0, 'ProgressBar': 0, 'VideoView': 0, 'ImageButton': 0,
                  'EditText': 0, 'RadioButton': 0, 'ToggleButton': 0}


ROOT_OUTPUT = "E:/Mulong/Datasets/rico/elements-14"
ROOT_IMG = 'E:/Mulong/Datasets/rico/combined'
PATH_LABEL = 'E:/Mulong/Datasets/rico/instances_train.json'
resize_ratio = 1


def setup_folder():
    for name in element_number:
        path = pjoin(ROOT_OUTPUT, name)
        if not os.path.exists(path):
            os.mkdir(path)


def fetch_and_clip(img, annotations, output_root, shrink_ratio=resize_ratio, pad=False, show_label=False, show_clip=False, write_clip=True):

    def padding(clip):
        height = np.shape(clip)[0]
        width = np.shape(clip)[1]

        pad_height = int(height / 10)
        pad_wid = int(width / 10)
        pad_img = np.full(((height + pad_height), (width + pad_wid), 3), 255, dtype=np.uint8)
        pad_img[int(pad_height / 2):(int(pad_height / 2) + height), int(pad_wid / 2):(int(pad_wid / 2) + width)] = clip
        return pad_img

    def shrink(img):
        img_shrink = cv2.resize(img, (int(img.shape[1] / shrink_ratio), int(img.shape[0] / shrink_ratio)))
        return img_shrink

    # 'x_min, y_min, x_max, y_max, element'
    for i in range(len(annotations['bboxes'])):
        bbox = annotations['bboxes'][i]
        if bbox[2] < 20 or bbox[3] < 20:
            continue
        element_name = element_map[str(annotations['categories'][i])]
        element_number[element_name] += 1

        clip = img[int(bbox[1]):int(bbox[1]+bbox[3]), int(bbox[0]):int(bbox[0]+bbox[2])]
        clip = shrink(clip)
        if pad:
            clip = padding(clip)

        if write_clip:
            cv2.imwrite(pjoin(output_root, element_name, str(element_number[element_name]) + '.png'), clip)
        if show_clip:
            cv2.imshow('clip', clip)
            cv2.waitKey(0)
        if show_label:
            cv2.rectangle(img, (int(bbox[0]), int(bbox[1])), (int(bbox[0]+bbox[2]), int(bbox[1]+bbox[3])), (0, 0, 255), 2)
            cv2.imshow('img', shrink(img))
            cv2.waitKey(0)


def load(file_name):
    def cvt_gt_annotations():
        annotations = {}
        for annot in data['annotations']:
            if annot['image_id'] not in annotations:
                annotations[annot['image_id']] = {'bboxes': [annot['bbox']], 'categories': [annot['category_id']]}
            else:
                annotations[annot['image_id']]['bboxes'].append(annot['bbox'])
                annotations[annot['image_id']]['categories'].append(annot['category_id'])
        return annotations

    data = json.load(open(file_name))
    images = data['images']
    annotations = cvt_gt_annotations()

    amount = len(images)
    bad = 0
    for i, image in enumerate(images):
        annots = annotations[image['id']]
        index = image['file_name'].split('/')[-1][:-4]
        img_path = pjoin(ROOT_IMG, index + '.jpg')
        try:
            print('Processing [%d/%d]:' % (i, amount), img_path)
            img = cv2.imread(img_path)
            img = cv2.resize(img, (image['width'], image['height']))
            fetch_and_clip(img, annots, ROOT_OUTPUT, show_label=False)
            print(element_number, '\n')
        except:
            bad += 1
            print('*** Bad Image :%d ***\n' % bad)


if __name__ == '__main__':
    setup_folder()
    load(PATH_LABEL)
    print(element_number)

