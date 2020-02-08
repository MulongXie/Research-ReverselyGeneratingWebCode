from os.path import join as pjoin
import os
import glob
import pandas as pd
import cv2
import numpy as np
import json

element_map = {'0':'Button', '1':'CheckBox', '2':'Chronometer', '3':'EditText', '4':'ImageButton', '5':'ImageView',
               '6':'ProgressBar', '7':'RadioButton', '8':'RatingBar', '9':'SeekBar', '10':'Spinner', '11':'Switch',
               '12':'ToggleButton', '13':'VideoView'}
element_number = {'ProgressBar': 1772, 'VideoView': 318, 'ImageView': 257824, 'RatingBar': 961, 'SeekBar': 1835,
                  'EditText': 14338, 'ToggleButton': 2716, 'Switch': 3231, 'ImageButton': 82689, 'Button': 38089,
                  'Spinner': 110, 'CheckBox': 8468, 'Chronometer': 56, 'RadioButton': 4941}
ROOT_OUTPUT = "E:/Mulong/Datasets/rico/elements-14"
ROOT_IMG = 'E:/Mulong/Datasets/rico/combined'
ROOT_LABEL = 'label_val.txt'


def setup_folder():
    for name in element_number:
        path = pjoin(ROOT_OUTPUT, name)
        if not os.path.exists(path):
            os.mkdir(path)


def fetch_and_clip(img, annotations, output_root, shrink_ratio=3, pad=False, show_label=False, show_clip=False, write_clip=True):

    def padding(clip):
        height = np.shape(clip)[0]
        width = np.shape(clip)[1]

        pad_height = int(height / 10)
        pad_wid = int(width / 10)
        pad_img = np.full(((height + pad_height), (width + pad_wid), 3), 255, dtype=np.uint8)
        pad_img[int(pad_height / 2):(int(pad_height / 2) + height), int(pad_wid / 2):(int(pad_wid / 2) + width)] = clip
        return pad_img

    def shrink(img, ratio=3.5):
        img_shrink = cv2.resize(img, (int(img.shape[1] / ratio), int(img.shape[0] / ratio)))
        return img_shrink

    # 'x_min, y_min, x_max, y_max, element'
    for annot in annotations:
        bbox = annot['bbox']
        if bbox[2] < 20 or bbox[3] < 20:
            continue
        element_name = element_map[str(annot['category_id'])]
        element_number[element_name] += 1

        clip = img[int(bbox[1]):int(bbox[1]+bbox[3]), int(bbox[0]):int(bbox[0]+bbox[2])]
        clip = cv2.resize(clip, (int(clip.shape[1] / shrink_ratio), int(clip.shape[0] / shrink_ratio)))
        if pad:
            clip = padding(clip)
        clip = shrink(clip)

        if write_clip:
            cv2.imwrite(pjoin(output_root, element_name, str(element_number[element_name]) + '.png'), clip)
        if show_clip:
            cv2.imshow('clip', clip)
            cv2.waitKey(0)
        if show_label:
            cv2.rectangle(img, (int(bbox[0]), int(bbox[1])), (int(bbox[0]+bbox[2]), int(bbox[1]+bbox[3])), (0, 0, 255), 2)
            cv2.imshow('img', shrink(img))
            cv2.waitKey(0)


def load(file_name='instances_train.json'):
    def get_all_annotations_by_img_id(img_id):
        select_annot = []
        for annotation in annotations:
            if annotation['image_id'] == img_id:
                select_annot.append(annotation)
        return select_annot

    data = json.load(open(file_name))
    images = data['images']
    annotations = data['annotations']

    start_point = '0'
    locate = False
    for i, image in enumerate(images):
        annots = get_all_annotations_by_img_id(image['id'])
        index = image['file_name'].split('/')[-1][:-4]
        img_path = pjoin(ROOT_IMG, index + '.jpg')
        if locate:
            if index != start_point:
                continue
            else:
                print('Start from ', start_point)
                locate = False

        print('Processing %d:' % i, img_path)
        img = cv2.imread(img_path)
        img = cv2.resize(img, (image['width'], image['height']))

        fetch_and_clip(img, annots, ROOT_OUTPUT, show_label=False)
        print(element_number, '\n')


setup_folder()
load()
print(element_number)
