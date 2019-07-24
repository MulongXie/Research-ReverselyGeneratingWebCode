import cv2
import glob
import numpy as np

import ip_preprocessing as pre


def split_word(img, hist, min_pix):
    front = -1
    is_word = False
    for cur, h in enumerate(hist):
        if not is_word and h > min_pix:
            front = cur
            is_word = True
            continue

        if is_word and h < min_pix:
            word = img[:, front:cur]
            is_word = False
            cv2.imshow('word', word)
            cv2.waitKey(0)
            cv2.destroyWindow('word')


clip_paths = glob.glob('output\\1\\*.png')

for clip_path in clip_paths:
    clip = cv2.imread(clip_path, 0)

    p = pre.preprocess(clip)
    hist = [int(h / 255) for h in np.sum(p, 0)]

    cv2.imshow('org', clip)
    split_word(clip, hist, 1)

    break
