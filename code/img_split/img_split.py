import cv2
import numpy as np
import pandas as pd

img = cv2.imread("D:\\datasets\\dataset_webpage\\data\\test\\screenshot\\0.png")
label = pd.read_csv("D:\\datasets\\dataset_webpage\\data\\test\\label\\0.csv")
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

    h += height_avg

print(mini_ranges)