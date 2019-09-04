
class Config:
    def __init__(self):
        self.image_shape = (64, 64, 3)
        self.class_map = ['button', 'input', 'select', 'search', 'list', 'img']
        self.class_number = len(self.class_map)

        self.DATA_PATH = "E:/Mulong/Datasets/dataset_webpage/elements"
        self.MODEL_PATH = 'E:/Mulong/Model/ui_compos/cnn3_img.h5'
