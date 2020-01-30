import cv2
import time

import block_division as div
import lib_uied.ip_preprocessing as pre
import lib_uied.ip_segment as seg
import lib_uied.ip_draw as draw
import lib_uied.ip_detection_utils as util
from config.MODEL_CNN import CNN
import ui
clf = CNN()
clf.load()

start = time.clock()

org, grey = pre.read_img('data/1.jpg', resize_h=600)

print(org.shape)

blocks_corner = div.block_division(grey)
blocks_clip = seg.clipping(org, blocks_corner, shrink=3)

for i in range(len(blocks_corner)):
    bin = pre.preprocess(blocks_clip[i])
    corners_block, corners_img, corners_compo, compos_class = ui.processing(blocks_clip[i], bin, clf)

    corners_img = util.corner_cvt_relative_position(corners_img, blocks_corner[i][0][0], blocks_corner[i][0][1])

    # draw_bounding = draw.draw_bounding_box_class(org, corners_compo, compos_class)
    # draw_bounding = draw.draw_bounding_box_class(draw_bounding, corners_block, ['block' for i in range(len(corners_block))])
    draw_bounding = draw.draw_bounding_box_class(org, corners_img, ['img' for i in range(len(corners_img))])

print(time.clock() - start)