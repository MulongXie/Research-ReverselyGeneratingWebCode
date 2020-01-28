import cv2

import lib_uied.ip_preprocessing as pre

org, grey = pre.read_img('data/1.jpg', 800)

print(org.shape)
cv2.imshow('org', org)
cv2.waitKey()