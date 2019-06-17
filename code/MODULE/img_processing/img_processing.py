import cv2
import numpy as np


def gradient_normal_float(img):
    row, column = img.shape
    img_f = np.copy(img)
    img_f = img_f.astype("float")

    gradient = np.zeros((row, column))
    for x in range(row - 1):
        for y in range(column - 1):
            gx = abs(img_f[x + 1, y] - img_f[x, y])
            gy = abs(img_f[x, y + 1] - img_f[x, y])
            gradient[x, y] = gx + gy
    gradient = gradient.astype("uint8")

    cv2.imshow("gradient", gradient)
    cv2.imwrite('gradient.png', gradient)
    cv2.waitKey(0)
    return gradient


def gradient_revised_int(img):
    row = np.shape(img)[0]
    column = np.shape(img)[1]

    grad = np.zeros(img.shape, dtype=np.uint8)
    for x in range(row - 1):
        for y in range(column - 1):
            gx = abs(img[x + 1, y] - img[x, y])
            gy = abs(img[x, y + 1] - img[x, y])
            grad[x, y] = gx + gy

    cv2.imwrite('grad_int.png', grad)
    cv2.waitKey(0)
    return grad


def grad_float_thresh(img):
    gradient = gradient_normal_float(img)
    rec, thresh = cv2.threshold(gradient, 0, 255, cv2.THRESH_BINARY)

    cv2.imshow("thresh", thresh)
    cv2.imwrite('thresh.png', thresh)
    cv2.waitKey(0)
    return thresh


img = cv2.imread("1.png", 0)
grad_float_thresh(img)