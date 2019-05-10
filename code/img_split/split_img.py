import cv2
import numpy as np
import pandas as pd

root_path = "D:\\datasets\\dataset_webpage\\data\\test\\"
output_path = root_path + "split\\"

img = cv2.imread(root_path + "screenshot\\1.png")
label = pd.read_csv(root_path + "label\\1.csv")
height_avg = 600

height_bottom = np.shape(img)[0]
print(height_bottom)

mini_ranges = []
mini_imgs = []

h = 0
while h < height_bottom:
    mini_range = {}

    mini_range['top'] = h
    mini_range['bottom'] = h + height_avg if h + height_avg <= height_bottom else height_bottom
    mini_ranges.append(mini_range)

    mini_img = img[mini_range['top']:mini_range['bottom'], :, :]
    mini_imgs.append(mini_img)
    cv2.imshow('img', mini_img)
    cv2.waitKey(0)
    cv2.imwrite(output_path + str(h) + '.png', mini_img)

    h += height_avg

print(mini_ranges)