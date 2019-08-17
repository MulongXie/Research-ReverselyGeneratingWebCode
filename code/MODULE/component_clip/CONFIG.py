from os.path import join as pjoin


class Config:

    def __init__(self):
        self.ROOT_INPUT = "E:\Mulong\Datasets\dataset_webpage\page10000"
        self.ROOT_OUTPUT = "E:\Mulong\Datasets\dataset_webpage\elements"
        self.ROOT_IMG_ORG = pjoin(self.ROOT_INPUT, "org")
        self.ROOT_IMG_SEGMENT = pjoin(self.ROOT_INPUT, "segment")
        self.ROOT_RELABEL = pjoin(self.ROOT_INPUT, "relabel")
