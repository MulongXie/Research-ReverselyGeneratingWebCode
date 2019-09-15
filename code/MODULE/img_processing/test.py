import cv2
import numpy as np


def gradient():
    img = cv2.imread("4.png")

    row, column = img.shape[:2]
    img_f = np.copy(img)
    # img_f = img_f.astype("float")

    gradient = np.zeros((row, column, 3))

    for x in range(row - 1):
        for y in range(column - 1):
            gx = abs(img_f[x + 1, y] - img_f[x, y])
            gy = abs(img_f[x, y + 1] - img_f[x, y])
            gradient[x, y] = gx + gy

    cv2.imwrite('ab.png', gradient)
    cv2.waitKey(0)


gradient()