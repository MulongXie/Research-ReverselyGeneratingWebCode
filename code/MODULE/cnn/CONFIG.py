
class Config:
    def __init__(self):
        self.image_shape = (64, 64, 3)
        self.class_number = 5
        self.class_map = ['Image', 'Icon', 'Button', 'Input']

        self.DATA_PATH = "E:/Mulong/Datasets/rico/elements"
        self.MODEL_PATH = 'E:/Mulong/Model/rico_compos/cnn1.h5'
