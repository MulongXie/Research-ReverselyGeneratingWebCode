import cv2
import numpy as np

img = cv2.imread('0.png')

cv2.imshow('img', img)
cv2.moveWindow('img', 2000, 100)
cv2.waitKey(0)