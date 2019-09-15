from os.path import join as pjoin
import os


class Config:

    def __init__(self):
        # Adjustable
        self.THRESHOLD_MIN_GRADIENT = 4
        self.THRESHOLD_OBJ_MIN_AREA = 175
        self.THRESHOLD_OBJ_MIN_PERIMETER = 70
        self.THRESHOLD_REC_MIN_EVENNESS = 0.66
        self.THRESHOLD_BLOCK_MIN_EDGE_LENGTH = 70   # dribbble:68 app:210 web:70
        self.THRESHOLD_UICOMPO_MAX_W_H_RATIO = 22   # dribbble:10 app:10 web:22

        # Frozen
        self.THRESHOLD_REC_MIN_EVENNESS_STRONG = 0.7
        self.THRESHOLD_REC_MAX_DENT_RATIO = 0.1
        self.THRESHOLD_BLOCK_MAX_BORDER_THICKNESS = 8
        self.THRESHOLD_BLOCK_MAX_CROSS_POINT = 0.3
        self.THRESHOLD_UICOMPO_MIN_W_H_RATIO = 0.4
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
