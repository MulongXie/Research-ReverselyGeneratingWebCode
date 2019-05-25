import cv2
import numpy as np

img = cv2.imread('sb.png')
row = np.shape(img)[0]
column = np.shape(img)[1]

grad = np.zeros(img.shape, dtype=np.uint8)

for x in range(row - 1):
    for y in range(column - 1):
        gx = abs(img[x + 1, y, :] - img[x, y, :])
        gy = abs(img[x, y + 1] - img[x, y, :])
        grad[x, y] = gx + gy

cv2.imwrite('bb.png', grad)
cv2.imshow("img", grad)
cv2.waitKey(0)