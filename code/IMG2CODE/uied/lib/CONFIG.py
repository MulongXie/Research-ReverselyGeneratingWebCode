from os.path import join as pjoin
import os


class Config:

    def __init__(self):
        # self.ROOT_INPUT = "E:\Mulong\Datasets\\Dribbble"
        # self.ROOT_OUTPUT = "E:\Mulong\Datasets\dataset_webpage\ip\ip_v9_dribbble_ctpn"
        # self.ROOT_INPUT = "D:\git_file\github\doing\Research-ReverselyGeneratingWebCode\code\IMG2CODE\data\input\googleplay"
        # self.ROOT_OUTPUT = "D:\git_file\github\doing\Research-ReverselyGeneratingWebCode\code\IMG2CODE\data\output\googleplay"
        self.ROOT_INPUT = "D:\git_file\github\doing\Research-ReverselyGeneratingWebCode\code\IMG2CODE\data\input\dribbble"
        self.ROOT_OUTPUT = "D:\git_file\github\doing\Research-ReverselyGeneratingWebCode\code\IMG2CODE\data\output\dribbble"
        self.ROOT_IMG_ORG = pjoin(self.ROOT_INPUT, "org")

        self.ROOT_LABEL_UIED = pjoin(self.ROOT_OUTPUT, "ui_label")
        self.ROOT_IMG_DRAWN_UIED = pjoin(self.ROOT_OUTPUT, "ui_img_drawn")
        self.ROOT_IMG_GRADIENT_UIED = pjoin(self.ROOT_OUTPUT, "ui_img_gradient")
        self.ROOT_LABEL_CTPN = pjoin(self.ROOT_OUTPUT, "ctpn_label")
        self.ROOT_IMG_DRAWN_CTPN = pjoin(self.ROOT_OUTPUT, "ctpn_drawn")
        self.ROOT_IMG_MERGE = pjoin(self.ROOT_OUTPUT, "merge_drawn")
        self.ROOT_IMG_COMPONENT = pjoin(self.ROOT_OUTPUT, "components")

        self.THRESHOLD_MIN_GRADIENT = 4
        self.THRESHOLD_OBJ_MIN_AREA = 175
        self.THRESHOLD_OBJ_MIN_PERIMETER = 70

        self.THRESHOLD_REC_MIN_EVENNESS = 0.7
        self.THRESHOLD_REC_MIN_EVENNESS_STRONG = 0.7
        self.THRESHOLD_REC_MAX_DENT_RATIO = 0.1

        self.THRESHOLD_BLOCK_MAX_BORDER_THICKNESS = 8
        self.THRESHOLD_BLOCK_MAX_CROSS_POINT = 0.3
        self.THRESHOLD_BLOCK_MIN_EDGE_LENGTH = 100

        self.THRESHOLD_UICOMPO_MIN_W_H_RATIO = 0.4
        self.THRESHOLD_UICOMPO_MAX_W_H_RATIO = 10

        self.THRESHOLD_TEXT_MAX_WORD_GAP = 10
        self.THRESHOLD_TEXT_MAX_HEIGHT = 100
        self.THRESHOLD_TEXT_MAX_WIDTH = 150

        self.THRESHOLD_LINE_THICKNESS = 5
        self.THRESHOLD_LINE_MIN_LENGTH_H = 50
        self.THRESHOLD_LINE_MIN_LENGTH_V = 50

        self.OCR_PADDING = 5
        self.OCR_MIN_WORD_AREA = 0.45

        self.COLOR = {'div': (0, 255, 0), 'img': (0, 0, 255), 'icon': (255, 166, 166), 'input': (255, 166, 0),
                      'text': (77, 77, 255), 'search': (255, 0, 166), 'list': (166, 0, 255), 'select': (166, 166, 166),
                      'button': (0, 166, 255)}

    def build_output_folders(self, is_clip):
        if not os.path.exists(self.ROOT_LABEL_UIED):
            os.mkdir(self.ROOT_LABEL_UIED)
        if not os.path.exists(self.ROOT_IMG_DRAWN_UIED):
            os.mkdir(self.ROOT_IMG_DRAWN_UIED)
        if not os.path.exists(self.ROOT_IMG_GRADIENT_UIED):
            os.mkdir(self.ROOT_IMG_GRADIENT_UIED)
        if not os.path.exists(self.ROOT_LABEL_CTPN):
            os.mkdir(self.ROOT_LABEL_CTPN)
        if not os.path.exists(self.ROOT_IMG_DRAWN_CTPN):
            os.mkdir(self.ROOT_IMG_DRAWN_CTPN)
        if not os.path.exists(self.ROOT_IMG_MERGE):
            os.mkdir(self.ROOT_IMG_MERGE)
        if is_clip and not os.path.exists(self.ROOT_IMG_COMPONENT):
            os.mkdir(self.ROOT_IMG_COMPONENT)
