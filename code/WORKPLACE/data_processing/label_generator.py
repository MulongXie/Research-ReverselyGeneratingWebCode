import cv2
import json
import numpy as np
from random import randint as rint
import pandas as pd
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
    # objs_json = json.dumps(objects)
    # open('objects.json', 'w').write(objs_json)
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


# ******* change here to fit new data format *******
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


if '__main__':
    # ****** change here ******
    # rico path
    path_img = 'E:\\Mulong\\Datasets\\rico\\combined\\'
    path_annot = 'E:\\Mulong\\Datasets\\rico\\semantic_annotations\\'
    # label path
    # data_train.csv / data_test.csv / data_val.csv
    ui_ids = pd.read_csv('data_train.csv', index_col=0)['UI Number'].values
    label_file = open('label_train.txt', 'a')
    # *************************

    i = 0
    for index in ui_ids:
        print(i, index)
        if os.path.exists(path_img + str(index) + '.jpg'):
            # extract Ui components, relabel them
            jfile = json.load(open(path_annot + str(index) + '.json', encoding="utf8"))
            old_compos = extract_objects(jfile)
            new_compos = recategorize(old_compos)
            # write out new label
            save_label(new_compos, path_img + str(index) + '.jpg', label_file)
            i += 1
    label_file.close()
