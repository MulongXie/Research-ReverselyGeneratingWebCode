from MODEL import CNN
from DATA import Data

# load data and generate training and testing data
data = Data()
data.load_data()
data.generate_training_data()

# build model
model = CNN()
# model.train(data)
model.evaluate(data)
# model.predict(['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png'], show=True)
