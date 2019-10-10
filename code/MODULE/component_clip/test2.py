import cv2

img1 = cv2.imread('ccl1.png')
img2 = cv2.imread('ccl2.png')

img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

cv2.imwrite('ccl2.png', img2)