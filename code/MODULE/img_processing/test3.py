import cv2
import numpy as np

img = cv2.imread('bb.png')

ret, bin = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)

open = cv2.morphologyEx(bin, cv2.MORPH_OPEN, (5, 5))

cv2.imshow('th', bin)
cv2.imwrite('ac.png', bin)
cv2.imshow('img', img)
cv2.waitKey(0)