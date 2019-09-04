import ip_detection as det
import ip_detection_utils as util
import ip_preprocessing as pre
import ip_draw as draw
import ip_segment as seg
import file_utils as file
import ocr_classify_text as ocr
from CONFIG import Config
from MODEL import CNN

import cv2
import time

start = time.clock()
# initialization
C = Config()
CNN = CNN()
CNN.load()
is_merge_img = False
is_shrink_img = True
is_save = True
is_clip = False


def pre_processing():
    # *** Step 1 *** pre-processing: gray, gradient, binary
    org, gray = pre.read_img('input/dribbble/9.png', (0, 3000))  # cut out partial img
    binary = pre.preprocess(gray, 3)
    return org, binary


def processing(org, binary):
    # *** Step 2 *** object detection: get connected areas -> get boundary -> get corners
    boundary_all, boundary_rec, boundary_nonrec = det.boundary_detection(binary)
    # get corner of boundaries
    corners_rec = det.get_corner(boundary_rec)
    corners_nonrec = det.get_corner(boundary_nonrec)

    # *** Step 3 *** data processing: identify blocks and imgs from rectangles -> identify compos -> identify irregular imgs
    corners_block, corners_img = det.img_or_block(org, binary, corners_rec)
    # identify potential buttons and input bars
    corners_block, corners_compo = det.uicomponent_or_block(org, corners_block)
    # shrink images with extra borders
    if is_shrink_img:
        corners_img = det.img_shrink(org, binary, corners_img)
    # identify irregular-shape img from irregular shapes
    corners_img += det.img_irregular(org, corners_nonrec)

    # *** Step 4 *** refine results: refine img according to size -> OCR text area filter
    corners_img = det.img_refine(org, corners_img)
    # merge overlapped corners, and remove nested corners
    if is_merge_img:
        corners_img = det.merge_corners(corners_img)
    # detect components in img
    # corners_compo += det.uicomponent_in_img(org, binary, corners_img) ******
    # remove pure text element
    corners_block = det.rm_text(org, corners_block)
    corners_img = det.rm_text(org, corners_img)
    corners_compo = det.rm_text(org, corners_compo)

    # *** Step 5 *** classification: clip and classify the potential components
    compos = seg.clipping(org, corners_compo)
    compos_classes = CNN.predict(compos)

    # *** Step 6 *** text detection from cleaned image
    img_clean = draw.draw_bounding_box(org, corners_img, color=(255, 255, 255), line=-1)
    corners_word = ocr.text_detection(org, img_clean)
    corners_sentence = ocr.text_merge_word_into_line(org, corners_word)

    return corners_block, corners_img, corners_compo, corners_sentence, compos_classes


def post_processing(org, binary, corners_block, corners_img, corners_compo, corners_sentence, compos_classes):
    # *** Step 7 *** post-processing: remove img elements from original image and segment into smaller size
    # draw results
    img_clean = draw.draw_bounding_box(org, corners_img, color=(255, 255, 255), line=-1)
    draw_bounding = draw.draw_bounding_box(org, corners_sentence, line=1)
    draw_bounding = draw.draw_bounding_box_class(draw_bounding, corners_block, ['block' for i in range(len(corners_block))])
    draw_bounding = draw.draw_bounding_box_class(draw_bounding, corners_img, ['img' for j in range(len(corners_img))])
    draw_bounding = draw.draw_bounding_box_class(draw_bounding, corners_compo, compos_classes)
    # save results
    if is_save:
        cv2.imwrite('output/org.png', org)
        cv2.imwrite('output/labeled.png', draw_bounding)
        cv2.imwrite('output/gradient.png', binary)
        cv2.imwrite('output/clean.png', img_clean)
        file.save_corners_json('output/compo.json', corners_block, ['div' for i in range(len(corners_block))])
        file.save_corners_json('output/compo.json', corners_img, ['img' for j in range(len(corners_img))])
        file.save_corners_json('output/compo.json', corners_compo, compos_classes)
    if is_clip:
        file.save_clipping(org, 'output/clip', corners_block, ['div' for k in range(len(corners_block))])
        file.save_clipping(org, 'output/clip', corners_img, ['img' for l in range(len(corners_img))])
        file.save_clipping(org, 'output/clip', corners_compo, compos_classes)


def in_img(org, binary, corners_block_org, corners_img_org, corners_compo_org, corners_sentence_org, compos_classes_org):
    pad = 2
    imgs = corners_img_org.copy()
    for corner in imgs:
        (top_left, bottom_right) = corner
        (col_min, row_min) = top_left
        (col_max, row_max) = bottom_right
        col_min = max(col_min - pad, 0)
        col_max = min(col_max + pad, org.shape[1])
        row_min = max(row_min - pad, 0)
        row_max = min(row_max + pad, org.shape[0])

        clip_org = org[row_min:row_max, col_min:col_max]
        clip_bin = binary[row_min:row_max, col_min:col_max]
        clip_bin = pre.reverse_binary(clip_bin)

        corners_block, corners_img, corners_compo, corners_sentence, compos_classes = processing(clip_org, clip_bin)
        corners_block_org += util.corner_cvt_relative_position(corners_block, col_min, row_min)
        corners_img_org += util.corner_cvt_relative_position(corners_img, col_min, row_min)
        corners_compo_org += util.corner_cvt_relative_position(corners_compo, col_min, row_min)
        corners_sentence_org += util.corner_cvt_relative_position(corners_sentence, col_min, row_min)
        compos_classes_org += compos_classes


def _main():
    org, binary = pre_processing()
    corners_block, corners_img, corners_compo, corners_sentence, compos_classes = processing(org, binary)
    in_img(org, binary, corners_block, corners_img, corners_compo, corners_sentence, compos_classes)
    post_processing(org, binary, corners_block, corners_img, corners_compo, corners_sentence, compos_classes)

    file.timer(start)


if __name__ == '__main__':
    _main()


