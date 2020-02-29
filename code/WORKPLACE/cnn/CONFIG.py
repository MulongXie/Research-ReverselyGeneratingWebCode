
class Config:
    def __init__(self):
        self.image_shape = (32, 32, 3)
        # self.class_map = ['Image', 'Icon', 'Button', 'Input']     # ele-4
        # self.class_map = ['Button', 'CheckBox', 'Chronometer', 'EditText', 'ImageButton', 'ImageView',
        #                   'ProgressBar', 'RadioButton', 'RatingBar', 'SeekBar', 'Spinner', 'Switch',
        #                   'ToggleButton', 'VideoView']            # ele-14

        # self.DATA_PATH = "E:/Mulong/Datasets/rico/elements-14"
        # self.MODEL_PATH = 'E:/Mulong/Model/rico_compos/cnn2-ele14.h5'

        # self.DATA_PATH = "E:\Mulong\Datasets\dataset_webpage\Components3"
        # self.MODEL_PATH = 'E:/Mulong/Model/rico_compos/cnn1-text.h5'

        # TEXT AND NON-TEXT
        # self.DATA_PATH = "E:\Mulong\Datasets\dataset_webpage\Components3"
        # self.MODEL_PATH = 'E:/Mulong/Model/rico_compos/cnn2-textview.h5'
        # self.class_map = ['Text', 'Non-Text']

        # NOISE RECOGNITION
        # self.DATA_PATH = "E:\Mulong\Datasets\dataset_webpage\Components3"
        # self.MODEL_PATH = 'E:/Mulong/Model/rico_compos/cnn1-noise.h5'
        # self.class_map = ['Noise', 'Non-Noise']

        # IMAGE RECOGNITION
        self.DATA_PATH = "E:\Mulong\Datasets\dataset_webpage\Components3"
        self.MODEL_PATH = 'E:/Mulong/Model/rico_compos/cnn-image-1.h5'
        self.class_map = ['Image', 'Non-Image']

        self.class_number = len(self.class_map)