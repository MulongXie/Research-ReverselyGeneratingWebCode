import cv2
import numpy as np


def find_contour():
    img = cv2.imread('bb.png')
    img = cv2.blur(img, (3,3))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

    binary, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 输出为三个参数
    cv2.drawContours(img, contours, -1, (0, 0, 255), 3)

    cv2.imshow("img", img)
    cv2.imwrite('bc.png', img)
    cv2.waitKey(0)


def gradient():
    img = cv2.imread("1.png", 0)

    row, column = img.shape
    img_f = np.copy(img)
    img_f = img_f.astype("float")

    gradient = np.zeros((row, column))

    for x in range(row - 1):
        for y in range(column - 1):
            gx = abs(img_f[x + 1, y] - img_f[x, y])
            gy = abs(img_f[x, y + 1] - img_f[x, y])
            gradient[x, y] = gx + gy

    sharp = img_f + gradient
    sharp = np.where(sharp < 0, 0, np.where(sharp > 255, 255, sharp))

    gradient = gradient.astype("uint8")
    sharp = sharp.astype("uint8")
    cv2.imshow("gradient", gradient)
    cv2.imwrite('aa.png', gradient)
    cv2.waitKey()