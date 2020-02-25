
class Config:
    def __init__(self):
        self.image_shape = (32, 32, 3)
        # self.class_map = ['Image', 'Icon', 'Button', 'Input']     # ele-4
        # self.class_map = ['Button', 'CheckBox', 'Chronometer', 'EditText', 'ImageButton', 'ImageView',
        #                   'ProgressBar', 'RadioButton', 'RatingBar', 'SeekBar', 'Spinner', 'Switch',
        #                   'ToggleButton', 'VideoView']            # ele-14
        self.class_map = ['Text', 'Non-Text']
        self.class_number = len(self.class_map)

        # self.DATA_PATH = "E:/Mulong/Datasets/rico/elements-14"
        self.DATA_PATH = "E:\Mulong\Datasets\dataset_webpage\Components3"
        self.MODEL_PATH = 'E:/Mulong/Model/rico_compos/cnn2-ele14.h5'
