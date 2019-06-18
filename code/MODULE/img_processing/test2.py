import cv2
import numpy as np

img = np.zeros((800, 600, 3), dtype=np.uint8)
img[30:50, 30:50, :] = 255
img[90:138, 50:76, :] = 255
img[100:103, 66:70] = 0

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
r, bin = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
cv2.imshow('bin', bin)
cv2.imshow('img', img)
cv2.waitKey(0)