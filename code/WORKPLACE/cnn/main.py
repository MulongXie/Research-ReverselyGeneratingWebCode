import cv2
import numpy as np

from CNN import CNN
from DATA import Data

# load data and generate training and testing data
# data = Data()
# data.load_data()
# data.generate_training_data()

# build model
model = CNN()
# model.train(data)
model.predict(['1.png', '0.png'], show=True)
# model.evaluate(data)
