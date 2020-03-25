import cv2
import lib_ip.ip_preprocessing as pre
import lib_ip.ip_detection as det


def nothing(x):
    pass


img_file = 'E:\\Mulong\\Datasets\\rico\\combined\\10019.jpg'
resize_height = 800

cv2.namedWindow('control')
cv2.createTrackbar('resize_height', 'control', 800, 1600, nothing)
cv2.createTrackbar('grad_min', 'control', 0, 255, nothing)
cv2.createTrackbar('kernel', 'control', 1, 10, nothing)

while 1:
    resize_height = cv2.getTrackbarPos('resize_height', 'control')
    grad_min = cv2.getTrackbarPos('grad_min', 'control')
    kernel = cv2.getTrackbarPos('kernel', 'control')

    org, gray = pre.read_img(img_file, resize_height)
    org = cv2.medianBlur(org, 1)
    binary = pre.preprocess(org, grad_min)

    # det.line_removal(binary, 8)

    # morph = cv2.morphologyEx(binary, cv2.MORPH_DILATE, (5, 5))
    # morph = cv2.morphologyEx(morph, cv2.MORPH_DILATE, (5, 5))
    # morph = cv2.morphologyEx(morph, cv2.MORPH_DILATE, (5, 5))

    cv2.imshow('org', org)
    cv2.imshow('bin', binary)
    cv2.imshow('no_line', binary)
    cv2.waitKey(10)
