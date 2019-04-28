# *** bug ***
# the importing image's size is changed when show by opencv
# *** provisional solution ***
# defining a distort parameter (0.66) to manually correct the size

import pandas as pd
import cv2
import numpy as np


def select_color(item):
    color = (0, 0, 0)
    if item == 'div':
        color = (0, 0, 200)
    elif item == 'input':
        color = (255, 0, 0)
    elif item == 'button':
        color = (180, 0, 0)
    elif item == 'h1':
        color = (0, 255, 0)
    elif item == 'h2':
        color = (0, 180, 0)
    elif item == 'p':
        color = (0, 100, 0)
    elif item == 'a':
        color = (200, 100, )
    elif item == 'img':
        color = (0, 100, 255)
    return color


def draw(pic):
    count = {}
    for i in range(0, len(df)):
        item = df.iloc[i]
        lp = (int(item.bx), int(item.by))
        rb = (int(item.bx + item.bw), int(item.by + item.bh))
        element = item.element

        color = select_color(item.element)
        if element in count:
            count[element] += 1
        else:
            count[element] = 1

        pic = cv2.rectangle(pic, lp, rb, color, 1)
        cv2.putText(pic, element + str(count[element]), (item.bx, item.by), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
    cv2.imwrite('draw.png', pic)


df = pd.read_csv('element0.csv')
img = cv2.imread('web.png')
distort = 1

img = cv2.resize(img, (int(np.shape(img)[1] * distort), int(np.shape(img)[0] * distort)))
draw(img)

print(np.shape(img))
cv2.imshow('img', img)
cv2.waitKey(0)