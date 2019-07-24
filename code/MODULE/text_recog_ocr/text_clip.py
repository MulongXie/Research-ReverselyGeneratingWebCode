import cv2
import glob
import os


def clip_text(img, label, output_path):
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    for i, l in enumerate(label.readlines()):
        if l is not '\n':
            pos = l[:-1].split(',')
            pos = [int(p) for p in pos]
            cv2.imwrite(os.path.join(output_path, str(i) + '.png'), img[pos[1]:pos[3], pos[0]:pos[2]])


label_paths = glob.glob('input/*.txt')

for label_path in label_paths:
    name = label_path.split('\\')[1][:-4]
    img_path = 'input/' + name + '.png'

    img = cv2.imread(img_path)
    label = open(label_path, 'r')
    print(img.shape)
    clip_text(img, label, os.path.join('output', name))

