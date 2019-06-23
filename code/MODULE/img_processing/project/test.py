import os
import cv2

input_root = 'input'
out_root = 'output'

for i in os.listdir(input_root):
    print(i)
    img = cv2.imread(os.path.join(input_root, i))
    cv2.imshow('img', img)
    cv2.waitKey(0)
