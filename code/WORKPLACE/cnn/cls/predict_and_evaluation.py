import json
import numpy as np
import cv2
from glob import glob
from os.path import join as pjoin
from tqdm import tqdm
import os

class_map = {'0':'Button', '1':'CheckBox', '2':'Chronometer', '3':'EditText', '4':'ImageButton', '5':'ImageView',
               '6':'ProgressBar', '7':'RadioButton', '8':'RatingBar', '9':'SeekBar', '10':'Spinner', '11':'Switch',
               '12':'ToggleButton', '13':'VideoView', '14':'TextView'}

def clipping(org, bbox, write_path=None, show=False, padding=(30, 20)):
    (column_min, row_min, column_max, row_max) = bbox
    column_min = max(column_min - padding[0], 0)
    column_max = min(column_max + padding[0], org.shape[1])
    row_min = max(row_min - padding[1], 0)
    row_max = min(row_max + padding[1], org.shape[0])
    clip = org[row_min:row_max, column_min:column_max]
    if show:
        cv2.imshow('clipping', clip)
        cv2.waitKey()
    if write_path is not None:
        cv2.imwrite(write_path, clip)
    return clip


def resize_label(bboxes, d_height, gt_height, bias=0):
    bboxes_new = []
    scale = gt_height / d_height
    for bbox in bboxes:
        bbox = [int(b * scale + bias) for b in bbox]
        bboxes_new.append(bbox)
    return bboxes_new


def draw_bounding_box(org, corners, color=(0, 255, 0), line=2, show=False):
    board = org.copy()
    for i in range(len(corners)):
        board = cv2.rectangle(board, (corners[i][0], corners[i][1]), (corners[i][2], corners[i][3]), color, line)
    if show:
        cv2.imshow('a', cv2.resize(board, (500, 1000)))
        cv2.waitKey(0)
    return board


def load_detect_result_json(reslut_file_root, shrink=0):
    def is_bottom_or_top(corner):
        column_min, row_min, column_max, row_max = corner
        if row_max < 36 or row_min > 725:
            return True
        return False

    result_files = glob(pjoin(reslut_file_root, '*.json'))
    compos_reform = {}
    print('Loading %d detection results' % len(result_files))
    for reslut_file in tqdm(result_files[:]):
        img_name = reslut_file.split('\\')[-1].split('.')[0]
        compos = json.load(open(reslut_file, 'r'))['compos']
        for compo in compos:
            if compo['column_max'] - compo['column_min'] < 10 or compo['row_max'] - compo['row_min'] < 10:
                continue
            if is_bottom_or_top((compo['column_min'], compo['row_min'], compo['column_max'], compo['row_max'])):
                continue
            if img_name not in compos_reform:
                compos_reform[img_name] = {'bboxes': [[compo['column_min'] + shrink, compo['row_min'] + shrink, compo['column_max'] - shrink, compo['row_max'] - shrink]],
                                           'categories': [compo['category']]}
            else:
                compos_reform[img_name]['bboxes'].append([compo['column_min'] + shrink, compo['row_min'] + shrink, compo['column_max'] - shrink, compo['row_max'] - shrink])
                compos_reform[img_name]['categories'].append(compo['category'])
    return compos_reform


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
            compos[img_name] = {'bboxes': [cvt_bbox(annot['bbox'])], 'categories': [class_map[str(annot['category_id'])]], 'size': size}
        else:
            compos[img_name]['bboxes'].append(cvt_bbox(annot['bbox']))
            compos[img_name]['categories'].append(class_map[str(annot['category_id'])])
    return compos


def eval(detection, ground_truth, img_root, cnn, show=False):
    store_gt_categories = []
    store_det_clips = []

    def match(org, d_bbox, gt_compos, matched):
        '''
        :param matched: mark if the ground truth component is matched
        :param d_bbox: [col_min, row_min, col_max, row_max]
        :param gt_bboxes: list of ground truth [[col_min, row_min, col_max, row_max]]
        :return: Boolean: if IOU large enough or detected box is contained by ground truth
        '''
        area_d = (d_bbox[2] - d_bbox[0]) * (d_bbox[3] - d_bbox[1])
        gt_bboxes = gt_compos['bboxes']
        gt_categories = gt_compos['categories']
        for i, gt_bbox in enumerate(gt_bboxes):
            if matched[i] == 0:
                continue
            area_gt = (gt_bbox[2] - gt_bbox[0]) * (gt_bbox[3] - gt_bbox[1])
            col_min = max(d_bbox[0], gt_bbox[0])
            row_min = max(d_bbox[1], gt_bbox[1])
            col_max = min(d_bbox[2], gt_bbox[2])
            row_max = min(d_bbox[3], gt_bbox[3])
            # if not intersected, area intersection should be 0
            w = max(0, col_max - col_min)
            h = max(0, row_max - row_min)
            area_inter = w * h
            if area_inter == 0:
                continue
            iod = area_inter / area_d
            iou = area_inter / (area_d + area_gt - area_inter)
            if iou > 0.9 or iod == 1:
                matched[i] = 0
                store_gt_categories.append(gt_categories[i])
                store_det_clips.append(clipping(org, d_bbox, show=show))
                return True
        return False

    amount = len(detection)
    FP, FN = 0, 0
    for i, image_id in enumerate(detection):
        img = cv2.imread(pjoin(img_root, image_id + '.jpg'))
        d_compos = detection[image_id]
        if image_id not in ground_truth:
            continue
        gt_compos = ground_truth[image_id]
        org_height = gt_compos['size'][0]

        d_compos['bboxes'] = resize_label(d_compos['bboxes'], 800, org_height)
        matched = np.ones(len(gt_compos['bboxes']), dtype=int)
        for d_bbox in d_compos['bboxes']:
            if not match(img, d_bbox, gt_compos, matched):
                FP += 1
        FN += sum(matched)

        print("[%d/%d]" % (i, amount))
        if i > 1000:
            break

    return store_det_clips, store_gt_categories, (FP, FN)


def evaluation(label_gt, label_pre, fp, fn, nontext=False):
    tp = 0
    for i in range(len(label_pre)):
        if nontext and (label_pre[i] == 'TextView' or label_gt[i] == 'TextView'):
            continue

        if label_gt[i] == label_pre[i]:
            tp += 1
        else:
            fp += 1
            fn += 1

    recall = tp/(tp + fp)
    precision = tp/(tp + fn)
    f1 = 2 * recall * precision / (recall + precision)

    print('Recall: %.3f; Precision: %.3f; F1: %.3f' %(recall, precision, f1))


from CNN import CNN
cnn = CNN('E:/Mulong/Model/rico_compos/cnn-rico-1.h5')

detect = load_detect_result_json('E:\\Mulong\\Result\\rico\\rico_uied\\rico_new_uied_cls\\merge')
gt = load_ground_truth_json('E:\\Mulong\\Datasets\\rico\\instances_test.json')
det_clips, gt_labels, (FP, FN) = eval(detect, gt, 'E:\\Mulong\\Datasets\\rico\\combined', cnn, show=False)

pre_labels = cnn.predict(det_clips)
evaluation(gt_labels, pre_labels, FP, FN, nontext=True)