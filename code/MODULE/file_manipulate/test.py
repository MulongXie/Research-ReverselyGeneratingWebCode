import cv2
import os
import numpy as np


def draw_box(img, box):
    count = 0
    for b in box:
        coord = b.split(",")
        coord = [int(c) for c in coord]
        img = cv2.rectangle(img, (coord[0], coord[1]), (coord[2], coord[3]), (0, 0, 255))
        cv2.putText(img, str(count), (coord[0], coord[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        count += 1


label = open('label.txt')

for l in label.readlines():
    content = l[:-1].split(" ")

    img_path = content[0]
    root_path = img_path[:(img_path.find('\segment'))]
    img_name = img_path[img_path.rfind('\\')+1:]
    write_path = os.path.join(root_path, 'labeled\\' + img_name)

    box = content[1:]
    img = cv2.imread(img_path)

    draw_box(img, box)
    cv2.imshow('i', img)
    cv2.waitKey(0)

