import cv2
import numpy as np

from MODEL import CNN
from DATA import Data

# load data and generate training and testing data
data = Data()
data.load_data(resize=True)
data.generate_training_data()

# build model
model = CNN()
model.train(data)

# MODEL.train(data)
# ms = ['1.png', '2.png', '3.png', '21.png', '22.png', '23.png', '24.png', '25.png']
# model = load_model('cnn1.h5')
# for m in ms:
#     img = cv2.imread(m)
#     img = cv2.resize(img, (64, 64))
#     img = np.reshape(img, (1, 64, 64, 3))
#     y = model.predict(img)
#     print(y)
