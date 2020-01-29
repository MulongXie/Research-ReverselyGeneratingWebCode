import cv2
import time

import block_division as div
import lib_uied.ip_preprocessing as pre
import lib_uied.ip_segment as seg
import lib_uied.ip_draw as draw
from lib_uied.MODEL_CNN import CNN
import ui
clf = CNN()
clf.load()

start = time.clock()

org, grey = pre.read_img('data/1.jpg', resize_h=600)

print(org.shape)

blocks_corner = div.block_division(grey)
blocks_clip = seg.clipping(org, blocks_corner, shrink=3)

for block in blocks_clip:
    bin = pre.preprocess(block)
    corners_block, corners_img, corners_compo, compos_class = ui.processing(block, bin, clf)
    draw_bounding = draw.draw_bounding_box_class(block, corners_compo, compos_class)
    draw_bounding = draw.draw_bounding_box_class(draw_bounding, corners_block, ['block' for i in range(len(corners_block))])
    draw_bounding = draw.draw_bounding_box_class(draw_bounding, corners_img, ['img' for i in range(len(corners_img))])

    cv2.imshow('bin', bin)
    cv2.imshow('b', draw_bounding)
    cv2.waitKey()

print(time.clock() - start)