from os.path import join as pjoin
import os


class Config:

    def __init__(self):
        self.ROOT_INPUT = "E:\Mulong\Datasets\\Dribbble"
        self.ROOT_OUTPUT = "E:\Mulong\Datasets\dataset_webpage\ip\ip_v7_dribbble_v2"
        self.ROOT_IMG_ORG = pjoin(self.ROOT_INPUT, "org")
        self.ROOT_LABEL = pjoin(self.ROOT_OUTPUT, "ip_label")
        self.ROOT_IMG_DRAWN = pjoin(self.ROOT_OUTPUT, "ip_img_drawn")
        self.ROOT_IMG_GRADIENT = pjoin(self.ROOT_OUTPUT, "ip_img_gradient")
        self.ROOT_IMG_CLEAN = pjoin(self.ROOT_OUTPUT, "ip_img_clean")
        self.ROOT_IMG_SEGMENT = pjoin(self.ROOT_OUTPUT, "ip_img_segment")

        self.THRESHOLD_MIN_GRADIENT = 3

        self.THRESHOLD_OBJ_MIN_AREA = 200
        self.THRESHOLD_OBJ_MIN_PERIMETER = 120

        self.THRESHOLD_REC_MIN_EVENNESS = 0.7
        self.THRESHOLD_REC_MIN_EVENNESS_STRONG = 0.75
        self.THRESHOLD_REC_MAX_DENT_RATIO = 0.1

        self.THRESHOLD_BLOCK_MAX_BORDER_THICKNESS = 8
        self.THRESHOLD_BLOCK_MAX_CROSS_POINT = 0.3
        self.THRESHOLD_BLOCK_MIN_EDGE_LENGTH = 100

        self.THRESHOLD_UICOMPO_MAX_EDGE_LENGTH = self.THRESHOLD_BLOCK_MIN_EDGE_LENGTH
        self.THRESHOLD_UICOMPO_MIN_EDGE_LENGTH = 30

        self.THRESHOLD_ICON_MAX_EDGE = 60

        self.THRESHOLD_IMG_MIN_EDGE_RATION = 2.5
        self.THRESHOLD_IMG_MIN_HEIGHT = 30

        self.THRESHOLD_TEXT_EDGE_RATIO = 2.5
        self.THRESHOLD_TEXT_MAX_WORD_GAP = 10
        self.THRESHOLD_TEXT_MAX_HEIGHT = 100
        self.THRESHOLD_TEXT_MAX_WIDTH = 150

        self.THRESHOLD_LINE_THICKNESS = 5
        self.THRESHOLD_LINE_MIN_LENGTH_H = 50
        self.THRESHOLD_LINE_MIN_LENGTH_V = 50

        self.OCR_PADDING = 5
        self.OCR_MIN_WORD_AREA = 0.3

        self.COLOR = {'block': (0, 255, 0), 'img': (0, 0, 255), 'icon': (255, 166, 166), 'input': (255, 166, 0),
                      'search': (255, 0, 166), 'list': (166, 0, 255), 'select': (166, 166, 166), 'button': (0, 166, 255)}

    def build_output_folders(self, is_segment):
        if not os.path.exists(self.ROOT_LABEL):
            os.mkdir(self.ROOT_LABEL)
        if not os.path.exists(self.ROOT_IMG_DRAWN):
            os.mkdir(self.ROOT_IMG_DRAWN)
        if not os.path.exists(self.ROOT_IMG_GRADIENT):
            os.mkdir(self.ROOT_IMG_GRADIENT)
        if not os.path.exists(self.ROOT_IMG_CLEAN):
            os.mkdir(self.ROOT_IMG_CLEAN)
        if is_segment and not os.path.exists(self.ROOT_IMG_SEGMENT):
            os.mkdir(self.ROOT_IMG_SEGMENT)