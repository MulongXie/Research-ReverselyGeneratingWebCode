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
is_classify = True
is_detect_line = False
is_ocr = True
is_segment = False
is_save = True

# *** Step 1 *** pre-processing: gray, gradient, binary
org, gray = pre.read_img('input/7.png', (0, 1000))  # cut out partial img
bin = pre.preprocess(gray, 1)


# *** Step 2 *** detect and remove lines: for better boundary detection
if is_detect_line:
    line_h, line_v = det.line_detection(bin,
                                        C.THRESHOLD_LINE_MIN_LENGTH_H, C.THRESHOLD_LINE_MIN_LENGTH_V,
                                        C.THRESHOLD_LINE_THICKNESS)
    bin_no_line = det.rm_line(bin, [line_h, line_v])
    binary = bin_no_line
else:
    binary = bin

# *** Step 3 *** get data: get connected areas -> get boundary -> get corners
boundary_all, boundary_rec, boundary_nonrec = det.boundary_detection(binary,
                                                        C.THRESHOLD_OBJ_MIN_AREA, C.THRESHOLD_OBJ_MIN_PERIMETER,        # size of area
                                                        C.THRESHOLD_LINE_THICKNESS,                                     # line check
                                                        C.THRESHOLD_REC_MIN_EVENNESS, C.THRESHOLD_IMG_MAX_DENT_RATIO)   # rectangle check
# get corner of boundaries
corners_rec = det.get_corner(boundary_rec)
corners_nonrec = det.get_corner(boundary_nonrec)


# *** Step 4 *** process data: identify blocks and imgs from rectangles -> identify compos -> identify irregular imgs
# identify rectangular block and rectangular img from rectangular shapes
corners_block, corners_img = det.img_or_block(org, binary, corners_rec,
                                              C.THRESHOLD_BLOCK_MAX_BORDER_THICKNESS, C.THRESHOLD_BLOCK_MAX_CROSS_POINT)  # block check
# identify potential buttons and input bars
corners_block, corners_compo = det.uicomponent_or_block(org, corners_block,
                                                        C.THRESHOLD_UICOMPO_MAX_HEIGHT, C.THRESHOLD_UICOMPO_MIN_EDGE_RATION)
# identify irregular-shape img from irregular shapes
corners_img += det.img_irregular(org, corners_nonrec,
                                 C.THRESHOLD_IMG_MUST_HEIGHT, C.THRESHOLD_IMG_MUST_WIDTH)   # img assertion


# *** Step 5 *** refine results: refine img according to size -> OCR text area filter
# ignore too large and highly likely text areas
corners_img = det.img_refine(org, corners_img,
                             C.THRESHOLD_IMG_MAX_HEIGHT_RATIO,                      # ignore too large imgs
                             C.THRESHOLD_TEXT_EDGE_RATIO, C.THRESHOLD_TEXT_HEIGHT)  # ignore text areas
# merge overlapped corners, and remove nested corners
# corners_img = det.merge_corners(corners_img)
# remove text
corners_block = det.rm_text(org, corners_block,
                          C.THRESHOLD_IMG_MUST_HEIGHT, C.THRESHOLD_IMG_MUST_WIDTH,    # img assertion
                          C.OCR_PADDING, C.OCR_MIN_WORD_AREA)                         # ignore text area
corners_img = det.rm_text(org, corners_img,
                          C.THRESHOLD_IMG_MUST_HEIGHT, C.THRESHOLD_IMG_MUST_WIDTH,    # img assertion
                          C.OCR_PADDING, C.OCR_MIN_WORD_AREA)                         # ignore text area
corners_compo = det.rm_text(org, corners_compo,
                          C.THRESHOLD_IMG_MUST_HEIGHT, C.THRESHOLD_IMG_MUST_WIDTH,    # img assertion
                          C.OCR_PADDING, C.OCR_MIN_WORD_AREA)                         # ignore text area


# *** Step 6 *** classification: clip and classify the potential components
if is_classify:
    CNN.load()
    compos = seg.clipping(org, corners_compo)
    compos_classes = CNN.predict(compos)
else:
    compos_classes = None


# *** Step 7 *** text detection from cleaned image
img_clean = draw.draw_bounding_box(org, corners_img, color=(255, 255, 255), line=-1)
if is_ocr:
    draw_bounding, word = ocr.text_detection(org, img_clean)
else:
    draw_bounding = org


# *** Step 8 *** post-processing: remove img elements from original image and segment into smaller size
if is_segment:
    seg.segment_img(img_clean, 600, 'output/segment')
# draw results
draw_bounding = draw.draw_bounding_box_class(draw_bounding, corners_block, ['block' for i in range(len(corners_block))], C.COLOR)
draw_bounding = draw.draw_bounding_box_class(draw_bounding, corners_img, ['img' for j in range(len(corners_img))], C.COLOR)
draw_bounding = draw.draw_bounding_box_class(draw_bounding, corners_compo, compos_classes, C.COLOR)
draw_boundary = draw.draw_boundary(boundary_rec, org.shape)
# save results
if is_save:
    cv2.imwrite('output/org.png', org)
    cv2.imwrite('output/labeled.png', draw_bounding)
    cv2.imwrite('output/boundary.png', draw_boundary)
    cv2.imwrite('output/gradient.png', bin)
    # cv2.imwrite('output/gradient_no_line.png', bin_no_line)
    cv2.imwrite('output/clean.png', img_clean)
    file.save_corners('output/corners.csv', corners_block, 'div')
    file.save_corners('output/corners.csv', corners_img, 'img', False)

end = file.timer(start)
