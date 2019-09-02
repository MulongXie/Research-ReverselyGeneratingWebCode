import cv2
import ip_preprocessing as pre
import draft

org, gray = pre.read_img('input/5.png', (0, 600))  # cut out partial img
binary = pre.preprocess(gray, 1)

binary_r = draft.reverse(binary)

cv2.imwrite('output/binary.png', binary)
cv2.imwrite('output/binary_r.png', binary_r)
