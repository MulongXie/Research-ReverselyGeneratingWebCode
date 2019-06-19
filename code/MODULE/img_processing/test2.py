import cv2
import numpy as np


img = np.zeros((600, 600, 3), dtype=np.uint8)
img[30:50, 30:50, :] = 255
img[90:138, 50:76, :] = 255
img[100:103, 66:70] = 0

print(img[1, :601, 1])

cv2.imshow('img', img)
cv2.waitKey(0)