import json
import cv2
from os.path import join as pjoin
from tqdm import tqdm


def draw_bounding_box(org, corners, color=(0, 0, 255), line=3, show=False):
    """
    Draw bounding box of components on the original image
    :param org: original image
    :param corners: [(top_left, bottom_right)]
                    -> top_left: (column_min, row_min)
                    -> bottom_right: (column_max, row_max)
    :param color: line color
    :param line: line thickness
    :param show: show or not
    :return: labeled image
    """
    board = org.copy()
    key = 0
    print('Number of bboxes:', len(corners))
    for i in range(len(corners)):
        board = cv2.rectangle(board, (corners[i][0], corners[i][1]), (corners[i][2], corners[i][3]), color, line)
    if show:
        cv2.imshow('a', cv2.resize(board, (300, 600)))
        key = cv2.waitKey(0)
    return board, key


def load_detect_result_json(annotation_file, data_file):
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

    data = json.load(open(data_file, 'r'))
    images = data['images']
    compos = {}
    annots = json.load(open(annotation_file, 'r'))
    print(len(annots))
    for i, annot in enumerate(tqdm(annots)):
        if annot['score'] < 0:
            continue
        img_name, size = get_img_by_id(annot['image_id'])
        if img_name not in compos:
            compos[img_name] = {'bboxes': [cvt_bbox(annot['bbox'])], 'categories': [annot['category_id']], 'size':size}
        else:
            compos[img_name]['bboxes'].append(cvt_bbox(annot['bbox']))
            compos[img_name]['categories'].append(annot['category_id'])

        if i > 1000000:
            break
    return compos


def load_ground_truth_json(annotation_file):
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

    data = json.load(open(annotation_file, 'r'))
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
        print("Number of bboxes:", len(annot['bbox']))
    return compos


def draw_gt(annots, img_root, show_gt=False):
    if show_gt:
        gts = load_ground_truth_json('E:\Mulong\Datasets\\rico/instances_val.json')

    for img_id in annots:
        img_file = pjoin(img_root, str(img_id) + '.jpg')
        img = cv2.imread(img_file)
        print(img_file)

        if show_gt:
            broad, _ = draw_bounding_box(img, gts[img_id]['bboxes'], color=(0,255,0), line=3)
        else:
            broad = img
        _, key = draw_bounding_box(broad, annots[img_id]['bboxes'], show=True, line=2)
        if key == ord('s'):
            cv2.destroyAllWindows()
            break


det = load_detect_result_json('E:\\Mulong\\Result\\rico\\centernet.json', 'E:/Mulong/Datasets/rico/instances_val.json')
draw_gt(det, 'E:\\Mulong\\Datasets\\rico\\combined')
