class Config:

    def __init__(self):
        self.DATA_ROOT = "D:/datasets/dataset_webpage/data/img_relabelled"
        self.LABEL_ROOT = "D:/datasets/dataset_webpage/data/img_relabelled/label"
        self.IMG_ROOT = "D:/datasets/dataset_webpage/data/img_relabelled/org"
        self.OUTPUT_ROOT = "D:/datasets/dataset_webpage/data/img_relabelled/IP_output"

        self.THRESHOLD_MIN_OBJ_AREA = 200
        self.THRESHOLD_MIN_REC_PARAMETER = 100
        self.THRESHOLD_MIN_REC_EVENNESS = 0.8
        self.THRESHOLD_MAX_EDGE_RATIO = 3
        self.THRESHOLD_MAX_BORDER_THICKNESS = 3
        self.THRESHOLD_MIN_LINE_THICKNESS = 10




