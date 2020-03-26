import cv2
from os.path import join as pjoin
import time
import numpy as np

import lib_ip.ip_preprocessing as pre
import lib_ip.ip_draw as draw
import lib_ip.block_division as blk
from config.CONFIG_UIED import Config
C = Config()


def block_detection(input_img_path, output_root,
                    num=0, resize_by_height=600, show=False, write_img=True):
    start = time.clock()
    name = input_img_path.split('\\')[-1][:-4]

    # *** Step 1 *** pre-processing: read img -> get binary map
    org, grey = pre.read_img(input_img_path, resize_by_height)

    # *** Step 2 *** block processing: detect block -> calculate hierarchy -> detect components in block
    blocks = blk.block_division(grey, org)
    blk.block_hierarchy(blocks)

    draw.draw_region(blocks, grey.shape, show=show, write_path=pjoin(output_root, name + '.png'))

    print("[Compo Detection Completed in %.3f s] %d %s" % (time.clock() - start, num, input_img_path))