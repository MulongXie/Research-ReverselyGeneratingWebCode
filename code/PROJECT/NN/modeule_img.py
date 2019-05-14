import cv2
import numpy as np

data_root = 'data/input/'


def read(imgname, meblursize=1):
    img = cv2.imread(imgname)
    img = cv2.resize(img, (64, 64))
    # img = cv2.medianBlur(img, meblursize)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img, gray_img


def padding(img):

    height = np.shape(img)[0]
    width = np.shape(img)[1]

    pad_height = int(height / 10)
    pad_wid = int(width / 10)
    pad_img = np.full(((height + pad_height), (width + pad_wid), 3), 255, dtype=np.uint8)
    pad_img[int(pad_height / 2):(int(pad_height / 2) + height), int(pad_wid / 2):(int(pad_wid / 2) + width)] = img

    return pad_img


def img_process():
    img, grey_img = read('1.png')
    pad_img = padding(img)
    cv2.imshow('img', pad_img)
    cv2.waitKey(0)


img_process()