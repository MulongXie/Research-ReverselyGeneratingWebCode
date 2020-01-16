import cv2
import json
import numpy as np
from random import randint as rint


def extract_objects_from_root(root):
    def extract(obj, layer):
        return {'layer':layer, 'class':obj['class'], 'bounds':obj['bounds'], 'rel-bounds':obj['rel-bounds']}

    def valid_obj(obj, rm_text=True):
        if 'visibility' in obj and obj['visibility'] == 'visible' and \
                'visible-to-user' in obj and obj['visible-to-user'] is True and \
                'Layout' not in obj['class'].split('.')[-1]:
            if rm_text:
                if 'Text' not in obj['class'].split('.')[-1]:
                    return True
                else:
                    return False
            return True
        else:
            return False

    def iter_kids(obj, layer):
        if valid_obj(obj):
            objects.append(extract(obj, layer))
        if 'children' in obj and len(obj['children']) > 0:
            children = obj['children']
            for child in children:
                iter_kids(child, layer + 1)

    objects = []
    iter_kids(root, 0)
    # save objects
    objs_json = json.dumps(objects)
    open('objects.json', 'w').write(objs_json)
    return objects


def view_objects(objects, org, shrink_ratio=5):
    def shrink(img, ratio):
        return cv2.resize(img, (int(img.shape[1] / ratio), int(img.shape[0] / ratio)))

    org = cv2.resize(org, (1440, 2560))
    org = shrink(org, shrink_ratio)
    cv2.imshow('original', org)

    board = np.zeros((2560, 1440, 3), dtype=np.uint8)
    for obj in objects:
        print(obj)
        color = (rint(0, 255), rint(0, 255), rint(0, 255))
        cv2.rectangle(board, (obj['bounds'][0], obj['bounds'][1]), (obj['bounds'][2], obj['bounds'][3]), color, -1)
        board_show = shrink(board, shrink_ratio)
        cv2.imshow('board_show', board_show)
        cv2.waitKey()
    print('end')
    cv2.waitKey()


index = '4'
imgfile = cv2.imread('E:\\Download\\combined\\' + index + '.jpg')
jfile = json.load(open('E:\\Download\\combined\\' + index + '.json'))

act = jfile['activity']
compos = extract_objects_from_root(act['root'])
view_objects(compos, imgfile)

