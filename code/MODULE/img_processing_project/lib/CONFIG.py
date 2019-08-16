from os.path import join as pjoin


class Config:

    def __init__(self):
        self.ROOT = "E:\Mulong\Datasets\dataset_webpage\page10000"
        self.ROOT_LABEL = pjoin(self.ROOT, "ip_label_rec")
        self.ROOT_IMG_ORG = pjoin(self.ROOT, "org")
        self.ROOT_IMG_DRAWN = pjoin(self.ROOT, "ip_img_drawn")
        self.ROOT_IMG_GRADIENT = pjoin(self.ROOT, "ip_img_gradient")
        self.ROOT_IMG_CLEAN = pjoin(self.ROOT, "ip_img_clean")
        self.ROOT_IMG_SEGMENT = pjoin(self.ROOT, "ip_img_segment")

        self.THRESHOLD_MIN_OBJ_AREA = 200
        self.THRESHOLD_MIN_OBJ_PERIMETER = 150
        self.THRESHOLD_MIN_REC_EVENNESS = 0.7

        self.THRESHOLD_MUST_IMG_HEIGHT = 100
        self.THRESHOLD_MUST_IMG_WIDTH = 150
        self.THRESHOLD_MAX_IMG_DENT_RATIO = 0.1
        self.THRESHOLD_MAX_IMG_HEIGHT_RATIO = 0.5

        self.THRESHOLD_MAX_BLOCK_BORDER_THICKNESS = 8
        self.THRESHOLD_MAX_BLOCK_CROSS_POINT = 0.3

        self.THRESHOLD_MIN_LINE_THICKNESS = 5
        self.THRESHOLD_MIN_LINE_LENGTH = 10

        self.THRESHOLD_TEXT_EDGE_RATIO = 2.5
        self.THRESHOLD_TEXT_HEIGHT = 20

        self.OCR_PADDING = 5
        self.OCR_MIN_WORD_AREA = 0.2
