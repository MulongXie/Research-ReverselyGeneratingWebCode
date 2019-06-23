import ip_detection as det
import ip_preprocessing as pre
import ip_draw as draw

import cv2
import time

start = time.clock()

org, gray = pre.read_img('1.png', (0, 2000))  # cut out partial img
binary = pre.preprocess(gray, 0)
boundary_all, boundary_rec = det.boundary_detection(binary)
corners = det.get_corner(boundary_rec)

bounding_drawn = draw.draw_bounding_box(corners, org)
boundary_drawn = draw.draw_boundary(boundary_all, org.shape)

print(time.clock() - start)  # running time

cv2.imwrite('bounding.png', bounding_drawn)
cv2.imwrite('boundary.png', boundary_drawn)
cv2.imwrite('gradient.png', binary)

# cv2.imshow('org', bounding_drawn)
# cv2.imshow('boundary', boundary_drawn)
# cv2.imshow('gradient', binary)
# cv2.waitKey(0)
