from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten, Dropout
from keras.utils import np_utils

from DATA import Data

data = Data()
data.load_data()

input_shape = data.image_shape
img_rows, img_cols = data.image_shape[:-2]
nb_classes = 4

