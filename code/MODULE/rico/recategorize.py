import cv2
import json
import numpy as np
from random import randint as rint
import os


def recategorize(objects):
    new_objects = []
    for obj in objects:
        if obj['compoLabel'] in ['Button Bar', 'Text Button', 'Radio Button']:
            obj['relabel'] = 'Button'
        elif obj['compoLabel'] in ['Image', 'Image Button']:
            obj['relabel'] = 'Image'
        elif obj['compoLabel'] in ['Input']:
            obj['relabel'] = 'Input'
        elif obj['compoLabel'] in ['Icon']:
            obj['relabel'] = 'Icon'
        else:
            continue
        new_objects.append(obj)
    return new_objects


def extract_objects_from_root(root):
    def extract(obj, layer):
        return {'class':obj['class'], 'bounds':obj['bounds'],
                'compoLabel':obj['componentLabel'] if 'componentLabel' in obj else None,
                'layer':layer}

    def iter_kids(obj, layer):
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


def labelling(objects, relabeled_objects, annotimg, org, shrink_ratio=4):
    def shrink(img, ratio):
        return cv2.resize(img, (int(img.shape[1] / ratio), int(img.shape[0] / ratio)))

    org = cv2.resize(org, (1440, 2560))
    annotimg = cv2.resize(annotimg, (1440, 2560))
    board = np.full((2560, 1440, 3), 255, dtype=np.uint8)

    for obj in objects:
        cv2.putText(annotimg, obj['compoLabel'], (int((obj['bounds'][0] + obj['bounds'][2])/2) - 50, int((obj['bounds'][1] + obj['bounds'][3])/2)),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 4)

    for obj in relabeled_objects:
        color = (rint(0, 255), rint(0, 255), rint(0, 255))
        cv2.rectangle(board, (obj['bounds'][0], obj['bounds'][1]), (obj['bounds'][2], obj['bounds'][3]), color, -1)
        cv2.putText(board, obj['relabel'], (int((obj['bounds'][0] + obj['bounds'][2]) / 2) - 50, int((obj['bounds'][1] + obj['bounds'][3]) / 2)),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)

    org = shrink(org, shrink_ratio)
    annot_show = shrink(annotimg, shrink_ratio)
    relabel_show = shrink(board, shrink_ratio)

    cv2.imshow('org', org)
    cv2.imshow('annotation', annot_show)
    cv2.imshow('relabeled', relabel_show)
    cv2.waitKey()


index = 0
while True:
    if os.path.exists('E:\\Download\\combined\\' + str(index) + '.jpg'):
        print(index)
        imgfile = cv2.imread('E:\\Download\\combined\\' + str(index) + '.jpg')
        jfile = json.load(open('E:\\Download\\semantic_annotations\\' + str(index) + '.json'))
        annofile = cv2.imread('E:\\Download\\semantic_annotations\\' + str(index) + '.png')

        compos = extract_objects_from_root(jfile)
        new_compos = recategorize(compos)
        labelling(compos, new_compos, annofile, imgfile)


    index += 1