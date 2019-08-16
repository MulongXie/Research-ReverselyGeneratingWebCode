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

        self.THRESHOLD_OBJ_MIN_AREA = 200
        self.THRESHOLD_OBJ_MIN_PERIMETER = 150
        self.THRESHOLD_REC_MIN_EVENNESS = 0.7

        self.THRESHOLD_IMG_MUST_HEIGHT = 100
        self.THRESHOLD_IMG_MUST_WIDTH = 150
        self.THRESHOLD_IMG_MAX_DENT_RATIO = 0.1
        self.THRESHOLD_IMG_MAX_HEIGHT_RATIO = 0.5

        self.THRESHOLD_BLOCK_MAX_BORDER_THICKNESS = 8
        self.THRESHOLD_BLOCK_MAX_CROSS_POINT = 0.3

        self.THRESHOLD_LINE_MIN_THICKNESS = 5

        self.THRESHOLD_TEXT_EDGE_RATIO = 2.5
        self.THRESHOLD_TEXT_HEIGHT = 20

        self.THRESHOLD_UICOMPO_MAX_HEIGHT = 100
        self.THRESHOLD_UICOMPO_MIN_EDGE_RATION = 1

        self.OCR_PADDING = 5
        self.OCR_MIN_WORD_AREA = 0.2
