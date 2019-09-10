import glob
from os.path import join as pjoin

from MODEL import CNN

model = CNN()
input = "E:/Mulong/Datasets/dataset_webpage/elements/text"
img_paths = glob.glob(pjoin(input, '*.png'))

model.predict(img_paths)