from os.path import join as pjoin


class Config:

    def __init__(self):
        self.ROOT_INPUT = "E:\Mulong\Datasets\dataset_webpage\page10000"
        self.ROOT_OUTPUT = "E:\Mulong\Datasets\dataset_webpage\ip\ip_v5_imgshrink"
        self.ROOT_IMG_ORG = pjoin(self.ROOT_INPUT, "org")
        self.ROOT_LABEL = pjoin(self.ROOT_OUTPUT, "ip_label")
        self.ROOT_IMG_DRAWN = pjoin(self.ROOT_OUTPUT, "ip_img_drawn")
        self.ROOT_IMG_GRADIENT = pjoin(self.ROOT_OUTPUT, "ip_img_gradient")
        self.ROOT_IMG_GRADIENT_NO_LINE = pjoin(self.ROOT_OUTPUT, "ip_img_gradient_no_line")
        self.ROOT_IMG_CLEAN = pjoin(self.ROOT_OUTPUT, "ip_img_clean")
        self.ROOT_IMG_SEGMENT = pjoin(self.ROOT_OUTPUT, "ip_img_segment")

        self.THRESHOLD_OBJ_MIN_AREA = 200
        self.THRESHOLD_OBJ_MIN_PERIMETER = 150
        self.THRESHOLD_REC_MIN_EVENNESS = 0.6

        self.THRESHOLD_IMG_MUST_HEIGHT = 100
        self.THRESHOLD_IMG_MUST_WIDTH = 150
        self.THRESHOLD_IMG_MAX_DENT_RATIO = 0.1
        self.THRESHOLD_IMG_MAX_HEIGHT_RATIO = 0.5

        self.THRESHOLD_BLOCK_MAX_BORDER_THICKNESS = 8
        self.THRESHOLD_BLOCK_MAX_CROSS_POINT = 0.3
        self.THRESHOLD_BLOCK_MIN_EDGE_LENGTH = 100

        self.THRESHOLD_LINE_THICKNESS = 5
        self.THRESHOLD_LINE_MIN_LENGTH_H = 50
        self.THRESHOLD_LINE_MIN_LENGTH_V = 50

        self.THRESHOLD_TEXT_EDGE_RATIO = 2.5
        self.THRESHOLD_TEXT_HEIGHT = 20

        self.THRESHOLD_UICOMPO_MAX_HEIGHT = 90
        self.THRESHOLD_UICOMPO_MIN_EDGE_RATION = 1

        self.OCR_PADDING = 5
        self.OCR_MIN_WORD_AREA = 0.3

        self.COLOR = {'block':(0, 255, 0), 'img':(0, 0, 255), 'button':(0, 166, 166), 'input':(255, 166, 0),
                      'search':(255, 0, 166), 'list':(166, 0, 255), 'select':(166, 166, 166), 'compo':(0, 166, 255)}
