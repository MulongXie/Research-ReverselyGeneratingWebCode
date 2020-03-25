import json
import numpy as np
import cv2
from glob import glob
from os.path import join as pjoin
from tqdm import tqdm

element_map = {'0':'Button', '1':'CheckBox', '2':'Chronometer', '3':'EditText', '4':'ImageButton', '5':'ImageView',
               '6':'ProgressBar', '7':'RadioButton', '8':'RatingBar', '9':'SeekBar', '10':'Spinner', '11':'Switch',
               '12':'ToggleButton', '13':'VideoView', '14':'TextView'}


def draw_bounding_box(org, compo, color=(0, 255, 0), line=2, show=False):
    board = org.copy()
    corners = compo['bboxes']
    labels = compo['categories']
    for i in range(len(corners)):
        cv2.rectangle(board, (corners[i][0], corners[i][1]), (corners[i][2], corners[i][3]), color, line)
        cv2.putText(board, str(labels[i]), (int((corners[i][0] + corners[i][2]) / 2), int((corners[i][1] + corners[i][3]) / 2)),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
    if show:
        cv2.imshow('a', cv2.resize(board, (300, 600)))
        cv2.waitKey(0)
    return board


def load_ground_truth_json(gt_file):
    def get_img_by_id(img_id):
        for image in images:
            if image['id'] == img_id:
                return image['file_name'].split('/')[-1][:-4], (image['height'], image['width'])

    def cvt_bbox(bbox):
        '''
        :param bbox: [x,y,width,height]
        :return: [col_min, row_min, col_max, row_max]
        '''
        bbox = [int(b) for b in bbox]
        return [bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]]

    data = json.load(open(gt_file, 'r'))
    images = data['images']
    annots = data['annotations']
    compos = {}
    print('Loading %d ground truth' % len(annots))
    for annot in tqdm(annots):
        img_name, size = get_img_by_id(annot['image_id'])
        if img_name not in compos:
            compos[img_name] = {'bboxes': [cvt_bbox(annot['bbox'])], 'categories': [annot['category_id']], 'size':size}
        else:
            compos[img_name]['bboxes'].append(cvt_bbox(annot['bbox']))
            compos[img_name]['categories'].append(annot['category_id'])
    return compos


gts = load_ground_truth_json('E:/Mulong/Datasets/rico/instances_val_notext.json')

index = '68011'
locate = True
for image_id in gts:
    if locate:
        if image_id != index:
            continue
        else:
            locate = False
    print(image_id)
    img = cv2.imread(pjoin('E:\\Mulong\\Datasets\\rico\\combined', image_id + '.jpg'))
    gt_compos = gts[image_id]
    cv2.imshow('org', cv2.resize(img, (300, 600)))
    draw_bounding_box(img, gt_compos, show=True)
