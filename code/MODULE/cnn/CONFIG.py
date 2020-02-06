
class Config:
    def __init__(self):
        self.image_shape = (32, 32, 3)
        self.class_number = 5
        self.class_map = ['Button', 'CheckBox', 'Chronometer', 'EditText', 'ImageButton', 'ImageView',
                          'ProgressBar', 'RadioButton', 'RatingBar', 'SeekBar', 'Spinner', 'Switch',
                          'ToggleButton', 'VideoView']  # ele-14
        # self.class_map = ['Image', 'Icon', 'Button', 'Input']

        self.DATA_PATH = "E:/Mulong/Datasets/rico/elements-14"
        self.MODEL_PATH = 'E:/Mulong/Model/rico_compos/cnn2-ele14.h5'
