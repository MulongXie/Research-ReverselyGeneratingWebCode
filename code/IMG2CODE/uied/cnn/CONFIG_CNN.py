
class Config:
    def __init__(self):
        self.image_shape = (64, 64, 3)
        self.class_map = ['button', 'input', 'icon', 'img', 'text']
        self.class_number = len(self.class_map)

        self.DATA_PATH = "E:/Mulong/Datasets/dataset_webpage/elements"
        self.MODEL_PATH = 'E:/Mulong/Model/ui_compos/cnn6_icon.h5'
        # self.MODEL_PATH = 'E:/Mulong/Model/ui_compos/cnn8.h5'
