import cv2
import numpy as np

moon = cv2.imread("1.png", 0)
row, column = moon.shape
moon_f = np.copy(moon)
moon_f = moon_f.astype("float")

gradient = np.zeros((row, column))

for x in range(row - 1):
    for y in range(column - 1):
        gx = abs(moon_f[x + 1, y] - moon_f[x, y])
        gy = abs(moon_f[x, y + 1] - moon_f[x, y])
        gradient[x, y] = gx + gy

gradient = gradient.astype("uint8")
cv2.imshow("moon", moon)
cv2.imshow("gradient", gradient)
cv2.waitKey()