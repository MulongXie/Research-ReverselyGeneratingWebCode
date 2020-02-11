import cv2
import lib_ip.ip_preprocessing as pre


def nothing(x):
    pass


img_file = 'data/input/29029.jpg'
resize_height = 800

cv2.namedWindow('control')
cv2.createTrackbar('resize_height', 'control', 400, 1600, nothing)
cv2.createTrackbar('grad_min', 'control', 0, 255, nothing)
cv2.createTrackbar('morph_peremeter', 'control', 1, 10, nothing)

while 1:
    resize_height = cv2.getTrackbarPos('resize_height', 'control')
    grad_min = cv2.getTrackbarPos('grad_min', 'control')
    morph_peremeter = cv2.getTrackbarPos('morph_peremeter', 'control')

    org, gray = pre.read_img(img_file, resize_height)
    binary_org = pre.preprocess(org, grad_min, (morph_peremeter, morph_peremeter))

    cv2.imshow('org', org)
    cv2.imshow('bin', binary_org)
    cv2.waitKey(10)