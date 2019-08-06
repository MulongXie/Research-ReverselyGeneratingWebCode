from os.path import join as pjoin


class Config:

    def __init__(self):
        self.ROOT = "E:\Mulong\Datasets\dataset_webpage\data1"
        self.ROOT_LABEL = pjoin(self.ROOT, "label_rec")
        self.ROOT_IMG_ORG = pjoin(self.ROOT, "img_org")
        self.ROOT_IMG_DRAWN = pjoin(self.ROOT, "img_drawn")
        self.ROOT_IMG_GRADIENT = pjoin(self.ROOT, "img_gradient")
        self.ROOT_IMG_CLEAN = pjoin(self.ROOT, "img_clean")
        self.ROOT_IMG_SEGMENT = pjoin(self.ROOT, "img_segment")

        self.THRESHOLD_MIN_OBJ_AREA = 200
        self.THRESHOLD_MIN_REC_PARAMETER = 100
        self.THRESHOLD_MIN_REC_EVENNESS = 0.8
        self.THRESHOLD_MAX_IMG_EDGE_RATIO = 2.2
        self.THRESHOLD_MIN_IMG_EDGE_LENGTH = 100
        self.THRESHOLD_MAX_BLOCK_BORDER_THICKNESS = 8
        self.THRESHOLD_MAX_BLOCK_CROSS_POINT = 0.1
        self.THRESHOLD_MIN_LINE_THICKNESS = 10




