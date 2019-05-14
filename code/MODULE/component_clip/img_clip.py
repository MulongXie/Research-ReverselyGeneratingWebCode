import cv2
import pandas as pd
import os
import numpy as np

input_root = 'D:\\datasets\\dataset_webpage\\data\\test\\'
output_root = 'component/test/'


def get_file():
    csv = []
    org_imgs = []
    for (root, _, file) in os.walk(input_root + 'label'):
        for f in file:
            csv.append(root + '/' + f)
    for (root, _, file) in os.walk(input_root + 'screenshot'):
        for f in file:
            org_imgs.append(root + '/' + f)
    return csv, org_imgs


def padding(img):

    height = np.shape(img)[0]
    width = np.shape(img)[1]

    pad_height = int(height / 10)
    pad_wid = int(width / 10)
    pad_img = np.full(((height + pad_height), (width + pad_wid), 3), 255, dtype=np.uint8)
    pad_img[int(pad_height / 2):(int(pad_height / 2) + height), int(pad_wid / 2):(int(pad_wid / 2) + width)] = img

    return pad_img


def clip(is_padding=False):

    csv, org_imgs = get_file()
    print(len(csv))
    print(len(org_imgs))

    count = {}
    for p in range(len(csv)):
        print(p)
        labels = pd.read_csv(csv[p])
        org_img = cv2.imread(org_imgs[p])

        for i in range(len(labels)):
            label = labels.iloc[i]

            compo_class = label.element
            component = org_img[int(label.by):int(label.by + label.bh), int(label.bx):int(label.bx + label.bw)]

            if label.bw == 0 or label.bh == 0 or label.bx < 0 or label.by < 0:
                continue
            if compo_class == 'a':
                continue
            if np.shape(component)[0] == 0 or np.shape(component)[1] == 0:
                continue

            if compo_class in count:
                count[compo_class] += 1
            else:
                count[compo_class] = 1

            if is_padding:
                component = padding(component)

            cv2.imwrite(output_root + compo_class + '/' +str(count[compo_class]) + '.png', component)


clip()
