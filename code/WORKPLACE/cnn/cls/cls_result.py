import json
from glob import glob
from os.path import join as pjoin
import cv2
import numpy as np
from tqdm import tqdm


color_map = {'Button': (0, 255, 0), 'CheckBox': (0, 0, 255), 'Chronometer': (255, 166, 166),
                      'EditText': (255, 166, 0),
                      'ImageButton': (77, 77, 255), 'ImageView': (255, 0, 166), 'ProgressBar': (166, 0, 255),
                      'RadioButton': (166, 166, 166),
                      'RatingBar': (0, 166, 255), 'SeekBar': (0, 166, 10), 'Spinner': (50, 21, 255),
                      'Switch': (80, 166, 66), 'ToggleButton': (0, 66, 80), 'VideoView': (88, 66, 0),
                      'TextView': (169, 255, 0)}


def draw_bounding_box(img, bboxes, classes, resize_height=800, line=2, show=False, write_path=None):
    def resize_by_height(org):
        w_h_ratio = org.shape[1] / org.shape[0]
        resize_w = resize_height * w_h_ratio
        re = cv2.resize(org, (int(resize_w), int(resize_height)))
        return re

    board = resize_by_height(img)
    for i, bbox in enumerate(bboxes):
        board = cv2.rectangle(board, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color_map[classes[i]], line)
        board = cv2.putText(board, classes[i], (bbox[0]+5, bbox[1]+20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.3, color_map[classes[i]], 2)
    if show:
        cv2.imshow('all', board)
        cv2.waitKey(0)
    if write_path is not None:
        cv2.imwrite(write_path, board)
    return board


def save_compos(file_path, bboxes, classes, new=True):
    if not new:
        f_in = open(file_path, 'r')
        output = json.load(f_in)
    else:
        output = {'compos': []}
    f_out = open(file_path, 'w')

    for i, bbox in enumerate(bboxes):
        c = {'category': classes[i]}
        (c['column_min'], c['row_min'], c['column_max'], c['row_max']) = bbox
        output['compos'].append(c)

    json.dump(output, f_out, indent=4)


def clipping(org, bboxes, show=False):
    clips = []
    for bbox in bboxes:
        (column_min, row_min, column_max, row_max) = bbox
        column_min = max(column_min, 0)
        column_max = min(column_max, org.shape[1])
        row_min = max(row_min, 0)
        row_max = min(row_max, org.shape[0])
        clip = org[row_min:row_max, column_min:column_max]
        clips.append(clip)
        if show:
            cv2.imshow('clipping', clip)
            cv2.waitKey()
    return clips


def view_detect_result_json(reslut_file_root, img_file_root, output_root, classifier=None, show=True):
    result_files = glob(pjoin(reslut_file_root, '*.json'))
    result_files = sorted(result_files, key=lambda x: int(x.split('\\')[-1].split('.')[0]))
    print('Loading %d detection results' % len(result_files))
    for reslut_file in tqdm(result_files):
        start_index = 3338
        end_index = 100000
        index = reslut_file.split('\\')[-1].split('.')[0]

        if int(index) < start_index:
            continue
        if int(index) > end_index:
            break

        org = cv2.imread(pjoin(img_file_root, index + '.jpg'))
        # print(index)
        compos = json.load(open(reslut_file, 'r'))['compos']
        bboxes = []
        for compo in compos:
            bboxes.append([compo['column_min'], compo['row_min'], compo['column_max'], compo['row_max']])

        if classifier is not None:
            classes = classifier.predict(clipping(org, bboxes))
        else:
            classes = np.full(len(bboxes), 'ImageView')

        if show:
            draw_bounding_box(org, bboxes, classes, show=True)

        save_compos(pjoin(output_root, index + '.json'), bboxes, classes)


result_path = 'E:\\Mulong\\Result\\rico\\rico_uied\\rico_new_uied_cls\\select'
image_path = "E:\\Mulong\\Datasets\\rico\\combined"
model_path = 'E:/Mulong/Model/rico_compos/resnet-ele14-45.h5'

output_root = 'E:\\Mulong\\Result\\rico\\rico_uied\\rico_new_uied_cls\\cls'

is_clf = True
if is_clf:
    from CNN import CNN
    classifier = CNN(model_path)
else:
    classifier = None

view_detect_result_json(result_path, image_path, output_root, classifier=classifier, show=False)
