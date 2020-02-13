import Resnet
import Data

# data = Data.Data()
# data.load_data(max_number=100)
# data.generate_training_data()

resnet = Resnet.ResClassifier()
# resnet.train(data)
root = 'E:/Mulong/Datasets/rico/elements-14-2/ToggleButton'
resnet.predict([root + '/{}.png'.format(i) for i in range(10)])