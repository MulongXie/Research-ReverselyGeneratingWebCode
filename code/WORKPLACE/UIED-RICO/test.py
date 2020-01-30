import lib_uied.ip_preprocessing as pre
import lib_uied.ip_draw as draw
import lib_uied.ip_detection as det
import lib_uied.ip_segment as seg
import lib_uied.file_utils as file
import lib_uied.ocr_classify_text as ocr
import lib_uied.ip_detection_utils as util
from config.CONFIG_UIED import Config

import cv2

# initialization
C = Config()
is_ocr = False
is_shrink_img = False


def processing_block(org, blocks_corner, classifier):
    blocks_clip = seg.clipping(org, blocks_corner, shrink=3)

    all_compos_boundary = []
    all_compos_corner = []
    all_compos_class = []

    for i in range(len(blocks_corner)):
        # get block information
        block_corner = blocks_corner[i]
        block_clip = blocks_clip[i]
        binary = pre.preprocess(block_clip)
        # extract components
        compos_boundary = det.boundary_detection(binary, rec_detect=False)
        compos_corner = det.get_corner(compos_boundary)
        # classify components
        compos_clip = seg.clipping(block_clip, compos_corner)
        compos_class = classifier.predict(compos_clip)
        # refine results
        compos_corner, compos_class = det.merge_corner(compos_corner, compos_class)
        compos_corner = util.corner_cvt_relative_position(compos_corner, block_corner[0][0], block_corner[0][1])

        if len(compos_boundary) > 0:
            all_compos_boundary += compos_boundary
            all_compos_corner += compos_corner
            all_compos_class += compos_class

    return all_compos_boundary, all_compos_corner, all_compos_class
