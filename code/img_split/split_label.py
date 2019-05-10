import cv2
import numpy as np
import pandas as pd

root_path = "D:\\datasets\\dataset_webpage\\data\\test\\"

label = pd.read_csv(root_path + "label\\0.csv")

print(len(label))

for i in range(len(label)):
    item = label.iloc[i]

    print("org:%d ; split:%d " %(item.by, item.by % 600))