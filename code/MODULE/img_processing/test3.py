import cv2

img = cv2.imread('c_close.png')
img = img[200: 480, 250:]

cv2.imshow('img', img)
cv2.waitKey(0)