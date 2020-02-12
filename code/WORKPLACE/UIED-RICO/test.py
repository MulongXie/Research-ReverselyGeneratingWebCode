import cv2
import lib_ip.ip_preprocessing as pre
import lib_ip.ip_detection as det


def nothing(x):
    pass


img_file = 'data/input/85.jpg'
resize_height = 800

cv2.namedWindow('control')
cv2.createTrackbar('resize_height', 'control', 800, 1600, nothing)
cv2.createTrackbar('grad_min', 'control', 0, 255, nothing)
cv2.createTrackbar('morph_peremeter', 'control', 1, 10, nothing)

while 1:
    resize_height = cv2.getTrackbarPos('resize_height', 'control')
    grad_min = cv2.getTrackbarPos('grad_min', 'control')
    morph_peremeter = cv2.getTrackbarPos('morph_peremeter', 'control')

    org, gray = pre.read_img(img_file, resize_height)
    binary = pre.preprocess(org, grad_min)
    binary_org = binary.copy()

    det.line_removal(binary, 8)

    # morph = cv2.morphologyEx(binary, cv2.MORPH_DILATE, (5, 5))
    # morph = cv2.morphologyEx(morph, cv2.MORPH_DILATE, (5, 5))
    # morph = cv2.morphologyEx(morph, cv2.MORPH_DILATE, (5, 5))

    cv2.imshow('org', org)
    cv2.imshow('bin', binary_org)
    cv2.imshow('no_line', binary)
    cv2.waitKey(10)
