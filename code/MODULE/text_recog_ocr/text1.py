import cv2
import glob
import numpy as np
import os

import ip_preprocessing as pre


def clip_sentence(img, label):
    sentences = []
    for i, l in enumerate(label.readlines()):
        if l is not '\n':
            pos = l[:-1].split(',')
            pos = [int(p) for p in pos]
            sentences.append(img[pos[1]:pos[3], pos[0]:pos[2]])

    return sentences


def clip_word(sentences, min_pix, output_path):
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    index = 0
    words = []
    for sentence in sentences:
        prepros = pre.preprocess(sentence)
        hist = [int(h / 255) for h in np.sum(prepros, 0)]   # project vertically

        front = -1
        is_word = False
        for cur, h in enumerate(hist):
            if not is_word and h > min_pix:
                front = cur
                is_word = True
                continue

            if is_word and h < min_pix:
                word = sentence[:, front:cur]
                words.append(word)
                is_word = False
                cv2.imwrite(os.path.join(output_path, str(index) + '.png'), word)
                index += 1
    return words


def main():
    label_paths = glob.glob('input/*.txt')

    for label_path in label_paths:
        name = label_path.split('\\')[1][:-4]
        img_path = 'input/' + name + '.png'

        img = cv2.imread(img_path, 0)
        label = open(label_path, 'r')

        sentences = clip_sentence(img, label)
        words = clip_word(sentences, 1, os.path.join('output', name))

        break


main()