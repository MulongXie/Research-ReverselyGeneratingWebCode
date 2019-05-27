import cv2
import os

data_position = 'D:\datasets\dataset_webpage\data'
root = os.path.join(data_position, 'img_segment')
img_root = os.path.join(root, 'img')
label_root = os.path.join(root, 'label')

labels = os.listdir(label_root)

index = [int(l[:-4]) for l in labels]

print(sorted(index))