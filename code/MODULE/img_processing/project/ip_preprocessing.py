import cv2
import numpy as np


def read_img(path, height=[0, 600]):
    img = cv2.imread(path, 0)
    img = img[height[0]:height[1]]
    return img


def get_gradient(img):
    row, column = img.shape[0], img.shape[1]
    img_f = np.copy(img)
    img_f = img_f.astype("float")

    gradient = np.zeros((row, column))
    for x in range(row - 1):
        for y in range(column - 1):
            gx = abs(img_f[x + 1, y] - img_f[x, y])
            gy = abs(img_f[x, y + 1] - img_f[x, y])
            gradient[x, y] = gx + gy
    gradient = gradient.astype("uint8")

    cv2.imwrite('gradient.png', gradient)
    return gradient


def grad_to_binary(grad):
    rec, bin = cv2.threshold(grad, 0, 255, cv2.THRESH_BINARY)
    return bin


def preprocess(img):
    grad = get_gradient(img)        # get RoI with high gradient
    binary = grad_to_binary(grad)   # enhance the RoI
    close = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, (5, 5))   # remove noises

    cv2.imwrite('binary.png', binary)
    cv2.imwrite('close.png', close)
    return close


img = read_img('2.png')
preprocess(img)