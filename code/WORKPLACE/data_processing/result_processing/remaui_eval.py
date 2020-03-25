import json
import numpy as np
import cv2
from glob import glob
from os.path import join as pjoin
from tqdm import tqdm


def resize_label(bboxes, gt_height, d_height=600):
    bboxes_new = []
    scale = gt_height/d_height
    for bbox in bboxes:
        bbox = [int(b * scale) for b in bbox]
        bboxes_new.append(bbox)
    return bboxes_new


def draw_bounding_box(org, corners, color=(0, 255, 0), line=2, show=False):
    board = org.copy()
    for i in range(len(corners)):
        board = cv2.rectangle(board, (corners[i][0], corners[i][1]), (corners[i][2], corners[i][3]), color, line)
    if show:
        cv2.imshow('a', cv2.resize(board, (300, 600)))
        cv2.waitKey(0)
    return board


def load_detect_result_txt(reslut_file_root):
    result_files = glob(pjoin(reslut_file_root, '*.txt'))
    compos_reform = {}
    print('Loading %d detection results' % len(result_files))
    for reslut_file in tqdm(result_files):
        file = open(reslut_file, 'r')
        for compos in file.readlines():
            img_name = compos.split()[0]
            compos = compos.split()[1:]
            for compo in compos:
                class_name = compo.split(',')[-1]
                compo = [int(c) for c in compo.split(',')[:-1]]

                if class_name == '4':
                   continue

                if img_name not in compos_reform:
                    compos_reform[img_name] = {'bboxes': [compo], 'categories': [class_name]}
                else:
                    compos_reform[img_name]['bboxes'].append(compo)
                    compos_reform[img_name]['categories'].append(class_name)
    return compos_reform


def load_result_multi_json(reslut_file_root):
    result_files = glob(pjoin(reslut_file_root, '*.json'))
    compos_reform = {}
    print('Loading %d detection results' % len(result_files))
    for reslut_file in tqdm(result_files):
        img_name = reslut_file.split('\\')[-1].split('.')[0]
        compos = json.load(open(reslut_file, 'r'))['compos']
        for compo in compos:
            if img_name not in compos_reform:
                compos_reform[img_name] = {'bboxes': [[compo['column_min'], compo['row_min'], compo['column_max'], compo['row_max']]]}
            else:
                compos_reform[img_name]['bboxes'].append([compo['column_min'], compo['row_min'], compo['column_max'], compo['row_max']])
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
        if int(annot['category_id']) == 14:
            continue
        if img_name not in compos:
            compos[img_name] = {'bboxes': [cvt_bbox(annot['bbox'])], 'categories': [annot['category_id']], 'size':size}
        else:
            compos[img_name]['bboxes'].append(cvt_bbox(annot['bbox']))
            compos[img_name]['categories'].append(annot['category_id'])
    return compos


def eval(detection, ground_truth, img_root, show=True):
    def match(org, d_bbox, gt_bboxes, matched):
        '''
        :param matched: mark if the ground truth component is matched
        :param d_bbox: [col_min, row_min, col_max, row_max]
        :param gt_bboxes: list of ground truth [[col_min, row_min, col_max, row_max]]
        :return: Boolean: if IOU large enough or detected box is contained by ground truth
        '''
        area_d = (d_bbox[2] - d_bbox[0]) * (d_bbox[3] - d_bbox[1])
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

            # if show:
            #     print("IoDetection: %.3f, IoU: %.3f" % (iod, iou))
            #     broad = draw_bounding_box(org, [d_bbox], color=(0, 0, 255))
            #     draw_bounding_box(broad, [gt_bbox], color=(0, 255, 0), show=True)

            if iou > 0.9 or iod == 1:
                matched[i] = 0
                return True
        return False

    amount = len(detection)
    TP, FP, FN = 0, 0, 0
    for i, image_id in enumerate(detection):
        img = cv2.imread(pjoin(img_root, image_id + '.jpg'))
        d_compos = detection[image_id]
        gt_compos = ground_truth[image_id]
        d_compos['bboxes'] = resize_label(d_compos['bboxes'], gt_compos['size'][0])
        matched = np.ones(len(gt_compos['bboxes']), dtype=int)
        for d_bbox in d_compos['bboxes']:
            if match(img, d_bbox, gt_compos['bboxes'], matched):
                TP += 1
            else:
                FP += 1
        FN += sum(matched)

        precesion = TP / (TP+FP)
        recall = TP / (TP+FN)
        if show:
            print("Number of gt boxes: %d, Number of detected boxes: %d" % (
            len(gt_compos['bboxes']), len(d_compos['bboxes'])))
            broad = draw_bounding_box(img,  d_compos['bboxes'], color=(255, 0, 0), line=2)
            draw_bounding_box(broad, gt_compos['bboxes'], color=(0, 0, 255), show=show, line=2)
            print('[%d/%d] TP:%d, FP:%d, FN:%d, Precesion:%.3f, Recall:%.3f' % (i, amount, TP, FP, FN, precesion, recall))

        if i % 20 == 0:
            print('[%d/%d] TP:%d, FP:%d, FN:%d, Precesion:%.3f, Recall:%.3f' % (i, amount, TP, FP, FN, precesion, recall))


# detect = load_detect_result_txt('E:\\Mulong\\Result\\rico\\rico_remaui_json')
detect = load_result_multi_json('E:\\Mulong\\Result\\rico\\rico_remaui_json')
gt = load_ground_truth_json('E:/Mulong/Datasets/rico/instances_test_nontext.json')
eval(detect, gt, 'E:\\Mulong\\Datasets\\rico\\combined', show=False)
