import os
import numpy as np
import pandas as pd

root = "D:/datasets/dataset_webpage/data"

csv = pd.read_csv('0.csv')

print(csv)

name = 0
path = os.path.join(root, "segment/img/" + str(name) + '/labeled')

print(path)

imgs = os.listdir(path)

print(imgs)