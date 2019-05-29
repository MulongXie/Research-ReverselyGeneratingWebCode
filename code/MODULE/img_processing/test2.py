import cv2
import numpy as np

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