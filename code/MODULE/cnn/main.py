import cv2
import numpy as np

from MODEL import CNN
from DATA import Data

# load data and generate training and testing data
data = Data()
data.load_data()
data.generate_training_data()

# build model
model = CNN()
# model.train(data)
# model.predict(['1.png', '2.png', '3.png', '21.png', '22.png', '23.png', '24.png', '25.png'], show=True)
model.evaluate(data)