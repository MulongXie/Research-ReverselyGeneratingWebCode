import ip_detection as det
import ip_preprocessing as pre
import ip_draw as draw
import ip_segment as seg
import file_utils as file
import ocr_classify_text as ocr

import cv2
import time

# initialization
start = time.clock()
is_detect_line = False
is_merge_img = False
is_shrink_img = False
is_ocr = True
is_segment = False
is_save = True

# *** Step 1 *** pre-processing: gray, gradient, binary
org, gray = pre.read_img('input/5.png', (0, 600))  # cut out partial img
binary = pre.preprocess(gray, 1)


# *** Step 2 *** object detection: get connected areas -> get boundary -> get corners
boundary_all, boundary_rec, boundary_nonrec = det.boundary_detection(binary)
# get corner of boundaries
corners_rec = det.get_corner(boundary_rec)
corners_nonrec = det.get_corner(boundary_nonrec)


# *** Step 3 *** process data: identify blocks and imgs from rectangles -> identify compos -> identify irregular imgs
# identify rectangular block and rectangular img from rectangular shapes
corners_block, corners_img = det.img_or_block(org, binary, corners_rec)
# identify potential buttons and input bars
corners_block, corners_compo = det.uicomponent_or_block(org, corners_block)
# shrink images with extra borders
if is_shrink_img:
    corners_img = det.img_shrink(org, binary, corners_img)
# identify irregular-shape img from irregular shapes
corners_img += det.img_irregular(org, corners_nonrec)
# ignore too large and highly likely text areas
corners_img = det.img_refine(org, corners_img)
# merge overlapped corners, and remove nested corners
if is_merge_img:
    corners_img = det.merge_corners(corners_img)
# detect components on img
corners_compo += det.uicomponent_in_img(org, binary, corners_img)
# remove text misrecognition
corners_block = det.rm_text(org, corners_block)
corners_img = det.rm_text(org, corners_img)
corners_compo = det.rm_text(org, corners_compo)


# *** Step 5 *** text detection from cleaned image
img_clean = draw.draw_bounding_box(org, corners_img, color=(255, 255, 255), line=-1)
if is_ocr:
    draw_bounding, word = ocr.text_detection(org, img_clean)
else:
    draw_bounding = org
img_clean = draw.draw_bounding_box(img_clean, corners_compo, color=(255, 255, 255), line=-1)


# *** Step 6 *** post-processing: remove img elements from original image and segment into smaller size
if is_segment:
    seg.segment_img(img_clean, 600, 'output/segment')
# draw results
draw_bounding = draw.draw_bounding_box_class(draw_bounding, corners_block, ['block' for i in range(len(corners_block))])
draw_bounding = draw.draw_bounding_box_class(draw_bounding, corners_img, ['img' for j in range(len(corners_img))])
draw_bounding = draw.draw_bounding_box_class(draw_bounding, corners_compo, ['compo' for j in range(len(corners_compo))])
draw_boundary = draw.draw_boundary(boundary_rec, org.shape)
# save results
if is_save:
    cv2.imwrite('output/org.png', org)
    cv2.imwrite('output/labeled.png', draw_bounding)
    cv2.imwrite('output/boundary.png', draw_boundary)
    cv2.imwrite('output/gradient.png', binary)
    cv2.imwrite('output/clean.png', img_clean)

end = file.timer(start)
