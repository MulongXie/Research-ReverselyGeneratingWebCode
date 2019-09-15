import ip_detection as det
import ip_preprocessing as pre
import ip_draw as draw
import ip_segment as seg
import file_utils as file
import ocr_classify_text as ocr
from CONFIG_UIED import Config

import cv2
import time

start = time.clock()
# initialization
is_ocr_check = False
is_shrink_img = False


def pre_processing(input_path, img_section):
    # *** Step 1 *** pre-processing: gray, gradient, binary
    org, gray = pre.read_img(input_path, img_section)  # cut out partial img
    binary = pre.preprocess(gray)
    return org, binary


def processing(org, binary, clf, main=True):
    if main:
        # *** Step 2 *** object detection: get connected areas -> get boundary -> get corners
        boundary_rec, boundary_non_rec = det.boundary_detection(binary)
        corners_rec = det.get_corner(boundary_rec)
        corners_non_rec = det.get_corner(boundary_non_rec)

        # *** Step 3 *** data processing: identify blocks and compos from rectangles -> identify irregular compos
        corners_block, corners_img, corners_compo = det.block_or_compo(org, binary, corners_rec)
        det.compo_irregular(org, corners_non_rec, corners_img, corners_compo)

        # *** Step 4 *** classification: clip and classify the components candidates -> ignore noises -> refine img
        compos = seg.clipping(org, corners_compo)
        compos_class = clf.predict(compos)
        corners_compo, compos_class = det.strip_img(corners_compo, compos_class, corners_img)

        # *** Step 5 *** result refinement
        if is_shrink_img:
            corners_img = det.img_shrink(org, binary, corners_img)

        # *** Step 6 *** recursive inspection: search components nested in components
        corners_block, corners_img, corners_compo, compos_class = det.compo_in_img(processing, org, binary, clf, corners_img, corners_block, corners_compo, compos_class)

        # *** Step 7 *** ocr check and text detection from cleaned image
        if is_ocr_check:
            corners_block, _ = det.rm_text(org, corners_block, ['block' for i in range(len(corners_block))])
            corners_img, _ = det.rm_text(org, corners_img, ['img' for i in range(len(corners_img))])
            corners_compo, compos_class = det.rm_text(org, corners_compo, compos_class)
            img_clean = draw.draw_bounding_box(org, corners_img, color=(255, 255, 255), line=-1)
            corners_word = ocr.text_detection(org, img_clean)
            corners_text = ocr.text_merge_word_into_line(org, corners_word)

        # *** Step 8 *** merge overlapped components
        # corners_img = det.rm_img_in_compo(corners_img, corners_compo)
        corners_img, _ = det.merge_corner(org, corners_img, ['img' for i in range(len(corners_img))], is_merge_nested_same=False)
        corners_compo, compos_class = det.merge_corner(org, corners_compo, compos_class, is_merge_nested_same=True)

        return corners_block, corners_img, corners_compo, compos_class

    # *** used for img inspection ***
    # only consider rectangular components
    else:
        boundary_rec, boundary_non_rec = det.boundary_detection(binary)
        corners_rec = det.get_corner(boundary_rec)
        corners_block, corners_img, corners_compo = det.block_or_compo(org, binary, corners_rec)
        compos = seg.clipping(org, corners_compo)
        compos_class = clf.predict(compos)
        corners_compo, compos_class = det.strip_img(corners_compo, compos_class, corners_img)

        return corners_block, corners_compo, compos_class
