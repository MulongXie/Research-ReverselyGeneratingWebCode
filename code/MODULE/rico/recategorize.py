import cv2
import json
import numpy as np
from random import randint as rint
import os


def extract_objects(root):
    '''
    read json files of annotation and extract components
    :param root: loaded jason object
    :return: UI components only containing class(original Android class), compoLabel(label defined in Rico paper 2) and bounds(topleft and bottomright)
    '''
    def extract(obj):
        return {'class':obj['class'], 'bounds':obj['bounds'],
                'compoLabel':obj['componentLabel'] if 'componentLabel' in obj else None}

    def iter_kids(obj):
        objects.append(extract(obj))
        if 'children' in obj and len(obj['children']) > 0:
            children = obj['children']
            for child in children:
                iter_kids(child)

    objects = []
    iter_kids(root)
    # save objects
    objs_json = json.dumps(objects)
    open('objects.json', 'w').write(objs_json)
    return objects


def recategorize(objects):
    '''
    relabel compoLabel into 4 classes: Button, Image, Icon and Input;
    filter out some improper annotations from Rico-semantic-annotation
    :param objects: UI components
    :return: selected components with new label
    '''
    new_objects = []
    for obj in objects:
        if (obj['bounds'][2] - obj['bounds'][0]) == 0 or (obj['bounds'][3] - obj['bounds'][1]) == 0:
            continue

        if obj['compoLabel'] in ['Radio Button']:
            obj['relabel'] = 'Button'
        elif obj['compoLabel'] in ['Icon']:
            obj['relabel'] = 'Icon'
        elif obj['compoLabel'] == 'Web View' and (obj['bounds'][3] - obj['bounds'][1]) > 500:
            return []

        elif obj['compoLabel'] in ['Image', 'Image Button', 'Video']:
            asp_ratio = (obj['bounds'][2] - obj['bounds'][0]) / (obj['bounds'][3] - obj['bounds'][1])
            asp_ratio = 1/asp_ratio if asp_ratio < 1 else asp_ratio
            if asp_ratio < 40:
                obj['relabel'] = 'Image'
            else:
                continue

        elif obj['compoLabel'] in ['Input'] and\
                'class' in obj and\
                'NumberPicker' not in obj['class'] and\
                'AppCompatEditText' not in obj['class']:
            obj['relabel'] = 'Input'

        elif obj['compoLabel'] in ['Text Button'] and\
                'class' in obj and\
                'TextView' not in obj['class'] and\
                'AppCompatButton' not in obj['class'] and\
                'CheckBox' not in obj['class'] and\
                'SwitchCompat' not in obj['class']:
            obj['relabel'] = 'Button'

        else:
            continue
        new_objects.append(obj)
    return new_objects


def save_label(objects, img_path, outputfile):
    '''
    save the new label as training format
    :param objects: UI components
    :param img_path: path of the related original image(UI screenshot)
    :param outputfile: file to output
    '''
    if len(objects) == 0:
        return
    compo_index = {'Image': 0, 'Icon': 1, 'Button': 2, 'Input': 3}
    label_txt = img_path + ' '
    for obj in objects:
        label_txt += ','.join([str(b) for b in obj['bounds']]) + ',' + str(compo_index[obj['relabel']]) + ' '
    label_txt += '\n'
    outputfile.write(label_txt)


def view_label(objects, relabeled_objects, annotimg, org, shrink_ratio=4):
    '''
    (Optional)
    visualize the annotations, new labels and original images
    :param objects: extracted UI components from original annotation
    :param relabeled_objects: relabeled UI components with new classes
    :param annotimg: original annotation image
    :param org: original screenshot image
    :param shrink_ratio: shrink all images in order to viewing conveniently
    '''
    def shrink(img, ratio):
        return cv2.resize(img, (int(img.shape[1] / ratio), int(img.shape[0] / ratio)))

    org = cv2.resize(org, (1440, 2560))
    annotimg = cv2.resize(annotimg, (1440, 2560))
    board = np.full((2560, 1440, 3), 255, dtype=np.uint8)  # used for draw new labels

    for obj in objects:
        cv2.putText(annotimg, obj['compoLabel'], (int((obj['bounds'][0] + obj['bounds'][2])/2) - 50, int((obj['bounds'][1] + obj['bounds'][3])/2)),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 4)

    for obj in relabeled_objects:
        color = (rint(0, 255), rint(0, 255), rint(0, 255))
        cv2.rectangle(board, (obj['bounds'][0], obj['bounds'][1]), (obj['bounds'][2], obj['bounds'][3]), color, -1)
        cv2.putText(board, obj['relabel'], (int((obj['bounds'][0] + obj['bounds'][2]) / 2) - 50, int((obj['bounds'][1] + obj['bounds'][3]) / 2)),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)

    # easy to show
    org = shrink(org, shrink_ratio)
    annot_show = shrink(annotimg, shrink_ratio)
    relabel_show = shrink(board, shrink_ratio)

    cv2.imshow('org', org)
    cv2.imshow('annotation', annot_show)
    cv2.imshow('relabeled', relabel_show)
    cv2.waitKey()


if '__main__':
    show = False
    start = 70000  # start point
    end = 70001
    index = start
    labelfile = open('label.txt', 'a')
    while True:
        if os.path.exists('E:\\Mulong\\Datasets\\rico\\combined\\' + str(index) + '.jpg'):
            print(index)
            # extract Ui components, relabel them
            jfile = json.load(open('E:\\Mulong\\Datasets\\rico\\semantic_annotations\\' + str(index) + '.json', encoding="utf8"))
            compos = extract_objects(jfile)
            new_compos = recategorize(compos)

            # read screenshot and drawn annotation image and show them
            if show:
                imgfile = cv2.imread('E:\\Mulong\\Datasets\\rico\\combined\\' + str(index) + '.jpg')
                annofile = cv2.imread('E:\\Mulong\\Datasets\\rico\\semantic_annotations\\' + str(index) + '.png')
                view_label(compos, new_compos, annofile, imgfile)

            # save new labels
            save_label(new_compos, 'E:\\Mulong\\Datasets\\rico\\combined\\' + str(index) + '.jpg', labelfile)

        index += 1
        if index > end:
            break
    labelfile.close()
