import cv2
import json
import numpy as np
from random import randint as rint


def extract_objects_from_root(root):
    def extract(obj, layer):
        return {'layer':layer, 'class':obj['class'], 'bound':obj['bounds'], 'rel-bounds':obj['rel-bounds']}

    def iter_kids(obj, layer):
        if 'visibility' in obj and obj['visibility'] == 'visible' and\
                'visible-to-user' in obj and obj['visible-to-user'] is True:
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


def view_objects(objects):
    def shrink(img, ratio):
        return cv2.resize(img, (int(img.shape[1] / ratio), int(img.shape[0] / ratio)))

    board = np.zeros((2560, 1440, 3), dtype=np.uint8)
    for obj in objects:
        print(obj)
        color = (rint(0, 255), rint(0, 255), rint(0, 255))
        cv2.rectangle(board, (obj['rel-bounds'][0], obj['rel-bounds'][1]), (obj['rel-bounds'][2], obj['rel-bounds'][3]),
                      color, -1)
        board_show = shrink(board, 3)
        cv2.imshow('board_show', board_show)
        cv2.waitKey()

    print('end')
    cv2.waitKey()


jfile = json.load(open('2.json'))
act = jfile['activity']
compos = extract_objects_from_root(act['root'])
view_objects(compos)

