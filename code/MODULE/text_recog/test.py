import cv2
import ip_preprocessing as pre

img = cv2.imread('input/3.png', 0)
grad = pre.gray_to_gradient(img)
bin = pre.grad_to_binary(grad, 1)

dilate = cv2.morphologyEx(bin, cv2.MORPH_DILATE, (5, 5))
dilate = cv2.morphologyEx(bin, cv2.MORPH_DILATE, (5, 5))
dilate = cv2.morphologyEx(bin, cv2.MORPH_DILATE, (5, 5))

cv2.imshow('a', bin)
cv2.imshow('d', dilate)
cv2.waitKey(0)

