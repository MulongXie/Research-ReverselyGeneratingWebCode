import cv2
import numpy as np

img = cv2.imread('bin2.png')

erode = cv2.erode(img, (3, 3))

cv2.imwrite('morph.png', erode)