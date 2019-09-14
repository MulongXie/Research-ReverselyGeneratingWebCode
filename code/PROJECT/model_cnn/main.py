from MODEL import CNN
from DATA import Data

# load data and generate training and testing data
# data = Data()
# data.load_data()
# data.generate_training_data()

# build model
model = CNN()
# model.train(data)
# model.evaluate(data)
model.predict(['9.png', '16.png', '37.png', '47.png', '58.png', '61.png', '89.png', '90.png'], show=True)
