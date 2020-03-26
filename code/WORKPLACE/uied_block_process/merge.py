import cv2
import json
import numpy as np
from random import randint as rint
import os


def rm_repeated_obj(objects):
    repeat = np.full(len(objects), False)
    objects_non_repeat = []
    for i in range(len(objects)):
        if not repeat[i]:
            for j in range(i + 1, len(objects) - 1):
                # print(objects[i]['bounds'], objects[j]['bounds'])
                if objects[i]['bounds'] == objects[j]['bounds']:
                    repeat[j] = True

    print(repeat)
    for i in range(len(repeat)):
        if not repeat[i]:
            objects_non_repeat.append(objects[i])
    return objects_non_repeat


def extract_objects(root):
    def extract(obj):
        return {'class':obj['class'], 'bounds':obj['bounds'],
                'compoLabel':obj['componentLabel'] if 'componentLabel' in obj else None}

    def iter_kids(obj):
        if obj['bounds'][2] - obj['bounds'][0] == 0 or obj['bounds'][3] - obj['bounds'][1] == 0:
            return
        objects.append(extract(obj))
        if 'children' in obj and len(obj['children']) > 0:
            children = obj['children']
            for child in children:
                iter_kids(child)

    objects = []
    if 'activity' in root:
        root = root['activity']['root']
    iter_kids(root)
    # save objects
    objs_json = json.dumps(objects)
    open('objects.json', 'w').write(objs_json)
    return objects


def view_label(objects, org, shrink_ratio=4):
    def shrink(img, ratio):
        return cv2.resize(img, (int(img.shape[1] / ratio), int(img.shape[0] / ratio)))

    org = cv2.resize(org, (1440, 2560))
    board = np.full((2560, 1440, 3), 255, dtype=np.uint8)  # used for draw new labels
    cv2.imshow('org', shrink(org, shrink_ratio))

    for i, obj in enumerate(objects):
        color = (rint(0, 255), rint(0, 255), rint(0, 255))
        cv2.rectangle(board, (obj['bounds'][0], obj['bounds'][1]), (obj['bounds'][2], obj['bounds'][3]), color, -1)
        cv2.putText(board, obj['class'], (int((obj['bounds'][0] + obj['bounds'][2]) / 2) - 50, int((obj['bounds'][1] + obj['bounds'][3]) / 2)),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)

        print(obj['bounds'], obj['bounds'][2] - obj['bounds'][0], obj['bounds'][3] - obj['bounds'][1])
        print('%d/%d: %s' %(i, len(objects), obj['class']))
        cv2.imshow('board', shrink(board, shrink_ratio))
        cv2.waitKey()

    # cv2.imshow('board', shrink(board, shrink_ratio))
    # cv2.waitKey()


if '__main__':
    save = False
    show = True
    start = 2  # start point
    end = 80000
    index = start
    input_root = 'E:\\Mulong\\Datasets\\rico\\combined\\'
    while True:
        img_path = input_root + str(index) + '.jpg'
        json_path = input_root + str(index) + '.json'
        if os.path.exists(img_path):
            print('\n', index)
            # extract Ui components, relabel them
            img = cv2.imread(img_path)
            jfile = json.load(open(json_path, encoding="utf8"))
            compos = extract_objects(jfile)
            compos = rm_repeated_obj(compos)

            if show:
                view_label(compos, img)

        index += 1
        if index > end:
            break