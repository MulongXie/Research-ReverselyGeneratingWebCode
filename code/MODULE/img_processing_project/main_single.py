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
is_merge_img = True
is_shrink_img = True
is_detect_compo_in_img = True
is_classify = True
is_ocr = True
is_segment = False
is_save = True
is_clip = False

if __name__ == '__main__':

    # *** Step 1 *** pre-processing: gray, gradient, binary
    org, gray = pre.read_img('input/69.png', (0, 2000))  # cut out partial img
    binary = pre.preprocess(gray, 1)

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
    if is_detect_compo_in_img:
        corners_compo += det.uicomponent_in_img(org, binary, corners_img)
    # remove pure text element
    corners_block = det.rm_text(org, corners_block)
    corners_img = det.rm_text(org, corners_img)
    corners_compo = det.rm_text(org, corners_compo)

    # *** Step 5 *** classification: clip and classify the potential components
    if is_classify:
        CNN.load()
        compos = seg.clipping(org, corners_compo)
        compos_classes = CNN.predict(compos)
    else:
        compos_classes = None

    # *** Step 6 *** text detection from cleaned image
    img_clean = draw.draw_bounding_box(org, corners_img, color=(255, 255, 255), line=-1)
    if is_ocr:
        draw_bounding, word = ocr.text_detection(org, img_clean)
    else:
        draw_bounding = org
    img_clean = draw.draw_bounding_box(img_clean, corners_compo, color=(255, 255, 255), line=-1)

    # *** Step 7 *** post-processing: remove img elements from original image and segment into smaller size
    if is_segment:
        seg.segment_img(img_clean, 600, 'output/segment')
    # draw results
    draw_bounding = draw.draw_bounding_box_class(draw_bounding, corners_block, ['block' for i in range(len(corners_block))])
    draw_bounding = draw.draw_bounding_box_class(draw_bounding, corners_img, ['img' for j in range(len(corners_img))])
    draw_bounding = draw.draw_bounding_box_class(draw_bounding, corners_compo, compos_classes)
    draw_boundary = draw.draw_boundary(boundary_rec, org.shape)
    # save results
    if is_save:
        cv2.imwrite('output/org.png', org)
        cv2.imwrite('output/labeled.png', draw_bounding)
        cv2.imwrite('output/boundary.png', draw_boundary)
        cv2.imwrite('output/gradient.png', binary)
        cv2.imwrite('output/clean.png', img_clean)
        file.save_corners_json('output/compo.json', corners_block, ['div' for i in range(len(corners_block))])
        file.save_corners_json('output/compo.json', corners_img, ['img' for j in range(len(corners_img))])
        file.save_corners_json('output/compo.json', corners_compo, compos_classes)
    if is_clip:
        file.save_clipping(org, 'output/clip', corners_block, ['div' for k in range(len(corners_block))])
        file.save_clipping(org, 'output/clip', corners_img, ['img' for l in range(len(corners_img))])
        file.save_clipping(org, 'output/clip', corners_compo, compos_classes)

    end = file.timer(start)
