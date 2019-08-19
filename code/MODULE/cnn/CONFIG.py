
class Config:
    def __init__(self):
        self.image_shape = (64, 64, 3)
        self.class_number = 5
        self.class_map = {'button': 0, 'input': 1, 'select': 2, 'search': 3, 'list': 4}

        self.DATA_PATH = "E:/Mulong/Datasets/dataset_webpage/elements"
        self.MODEL_PATH = 'E:/Mulong/Model/ui_compos/cnn2.h5'
