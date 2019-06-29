class Config:

    def __init__(self):
        self.DATA_ROOT = "D:/datasets/dataset_webpage/data/img_relabelled"
        self.LABEL_ROOT = "D:/datasets/dataset_webpage/data/img_relabelled/label"
        self.IMG_ROOT = "D:/datasets/dataset_webpage/data/img_relabelled/org"
        self.OUTPUT_ROOT = "D:/datasets/dataset_webpage/data/img_relabelled/IP_output"

        self.THRESHOLD_MIN_OBJ_AREA = 400
        self.THRESHOLD_MIN_REC_PARAMETER = 400
        self.THRESHOLD_MIN_REC_EVENNESS = 0.8
        self.THRESHOLD_MAX_BORDER_THICKNESS = 6
        self.THRESHOLD_MIN_BORDER_GAP = 10




