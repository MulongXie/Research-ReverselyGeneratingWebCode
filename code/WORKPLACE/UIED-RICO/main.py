import cv2
import time

import ip
import lib_ip.block_division as blk
import lib_ip.ip_preprocessing as pre
import lib_ip.ip_segment as seg
import lib_ip.ip_draw as draw
import lib_ip.ip_detection_utils as util
from config.MODEL_CNN import CNN
cnn = CNN()
cnn.load()

start = time.clock()

org, grey = pre.read_img('data/1.jpg', resize_h=600)
binary_org = pre.preprocess(org)

# divide layout blocks
blocks_corner = blk.block_division(grey)
# detect elements from blocks
compo_in_blk_boundary, compo_in_blk_corner, compo_in_blk_class = ip.processing_block(org, binary_org, blocks_corner, cnn)

# erase block parts
binary_non_block = blk.block_erase(binary_org, blocks_corner)
# detect elements from non-block parts
compo_non_blk_boundary, compo_non_blk_corner, compo_non_blk_class = ip.processing(org, binary_non_block, cnn, True)

# merge
compos_boundary = compo_in_blk_boundary + compo_non_blk_boundary
compos_corner = compo_in_blk_corner + compo_non_blk_corner
compos_class = compo_in_blk_class + compo_non_blk_class

draw_bounding = draw.draw_bounding_box_class(org, compos_corner, compos_class)
cv2.imshow('broad', draw_bounding)
cv2.waitKey()

print(time.clock() - start)