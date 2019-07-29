class Config:

    def __init__(self):
        self.ROOT_LABEL = "E:\Mulong\Datasets\dataset_webpage\label_rec"
        self.ROOT_IMG_ORG = "E:\Mulong\Datasets\dataset_webpage\img_org"
        self.ROOT_IMG_DRAWN = "E:\Mulong\Datasets\dataset_webpage\img_drawn"
        self.ROOT_IMG_GRADIENT = "E:\Mulong\Datasets\dataset_webpage\img_gradient"
        self.ROOT_IMG_CLEAN = "E:\Mulong\Datasets\dataset_webpage\img_clean"
        self.ROOT_IMG_SEGMENT = "E:\Mulong\Datasets\dataset_webpage\img_segment"

        self.THRESHOLD_MIN_OBJ_AREA = 50
        self.THRESHOLD_MIN_REC_PARAMETER = 100
        self.THRESHOLD_MIN_REC_EVENNESS = 0.8
        self.THRESHOLD_MAX_EDGE_RATIO = 2.2
        self.THRESHOLD_MAX_BORDER_THICKNESS = 5
        self.THRESHOLD_MIN_LINE_THICKNESS = 10




