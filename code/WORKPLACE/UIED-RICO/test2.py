import cv2
import time

import ip
import ui
import lib_uied.block_division as blk
import lib_uied.ip_preprocessing as pre
import lib_uied.ip_segment as seg
import lib_uied.ip_draw as draw
import lib_uied.ip_detection_utils as util
from config.MODEL_CNN import CNN
cnn = CNN()
cnn.load()

start = time.clock()

org, grey = pre.read_img('data/1.jpg', resize_h=600)

blocks_corner = blk.block_division(grey)
compo_in_blk_boundary, compo_in_blk_corner, compo_in_blk_class = ip.processing_block(org, blocks_corner, cnn)

draw_bounding = draw.draw_bounding_box_class(org, compo_in_blk_corner, compo_in_blk_class)
cv2.imshow('broad', draw_bounding)
cv2.waitKey()

print(time.clock() - start)