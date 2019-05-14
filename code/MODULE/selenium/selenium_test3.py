import cv2
import numpy as np

img = cv2.imread('long.png')

print(np.shape(img))

img2 = cv2.rectangle(img, (0, 200), (1000, 6000), (255, 0, 0), 2)

cv2.imwrite('./a.png', img2)

cv2.imshow('img', img2)
cv2.waitKey(0)

