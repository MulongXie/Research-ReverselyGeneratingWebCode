import ip_detection as det
import ip_preprocessing as pre
import ip_draw as draw
import ip_segment as seg
import file_utils as file
import ocr_classify_text as ocr
from CONFIG import Config
from MODEL import CNN

import cv2
import time

# initialization
C = Config()
CNN = CNN()
start = time.clock()
is_classify = True
is_detect_line = False
is_merge_img = False
is_ocr = True
is_segment = False
is_save = True

org, gray = pre.read_img('input/0.png', (0, 3000))  # cut out partial img
bin = pre.preprocess(gray, 1)

line_h, line_v = det.line_detection(bin,
                                    C.THRESHOLD_LINE_MIN_LENGTH_H, C.THRESHOLD_LINE_MIN_LENGTH_V,
                                    C.THRESHOLD_LINE_THICKNESS)
print(len(line_h), len(line_v))
draw.draw_line(org, (line_h, line_v), (0,0,255))
cv2.imwrite('output/line.png', org)