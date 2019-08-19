import ip_detection as det
import ip_preprocessing as pre
import ip_draw as draw
import ip_segment as seg
import file_utils as file
from CONFIG import Config
from MODEL import CNN

import cv2
import time
import glob
from os.path import join as pyjoin

# initialization
C = Config()
input_root = C.ROOT_IMG_ORG
input_paths = glob.glob(pyjoin(input_root, '*.png'))
input_paths = sorted(input_paths, key=lambda x: int(x.split('\\')[-1][:-4]))  # sorted by index
file.build_output_folders(C)
CNN = CNN()
CNN.load()

is_classify = True
is_save = True
start_index = 18
end_index = 18

for input_path in input_paths:
    index = input_path.split('\\')[-1][:-4]
    if int(index) < start_index:
        continue
    if int(index) > end_index:
        break

    start = time.clock()

    # set paths
    print(input_path)
    print(time.ctime())
    out_img_draw = pyjoin(C.ROOT_IMG_DRAWN, index + '.png')
    out_img_clean = pyjoin(C.ROOT_IMG_CLEAN, index + '.png')
    out_img_gradient = pyjoin(C.ROOT_IMG_GRADIENT, index + '.png')
    out_img_segment = pyjoin(C.ROOT_IMG_SEGMENT, index)
    out_label = pyjoin(C.ROOT_LABEL, index + '.csv')

    # *** Step 1 *** pre-processing:
    # gray, gradient, binary
    org, gray = pre.read_img(input_path, (0, 3000))  # cut out partial img
    if org is None or gray is None: continue
    binary = pre.preprocess(gray, 1)

    # *** Step 2 *** get data:
    # get connected areas -> get boundary -> get corners
    boundary_all, boundary_rec, boundary_nonrec = det.boundary_detection(binary,
                                                      C.THRESHOLD_OBJ_MIN_AREA, C.THRESHOLD_OBJ_MIN_PERIMETER,       # size of area
                                                      C.THRESHOLD_LINE_MIN_THICKNESS,                                # line check
                                                      C.THRESHOLD_REC_MIN_EVENNESS, C.THRESHOLD_IMG_MAX_DENT_RATIO)  # rectangle check
    # get corner of boundaries
    corners_rec = det.get_corner(boundary_rec)
    corners_nonrec = det.get_corner(boundary_nonrec)

    # *** Step 3 *** process data:
    # identify blocks and imgs from rectangles -> identify compos -> identify irregular imgs
    # identify rectangular block and rectangular img from rectangular shapes
    corners_block, corners_img = det.img_or_block(org, binary, corners_rec,
                                      C.THRESHOLD_BLOCK_MAX_BORDER_THICKNESS, C.THRESHOLD_BLOCK_MAX_CROSS_POINT)  # block check
    # identify potential buttons and input bars
    corners_block, corners_compo = det.uicomponent_or_block(org, corners_block,
                                       C.THRESHOLD_UICOMPO_MAX_HEIGHT,  C.THRESHOLD_UICOMPO_MIN_EDGE_RATION)   # components shape
    # identify irregular-shape img from irregular shapes
    corners_img += det.img_irregular(org, corners_nonrec,
                                     C.THRESHOLD_IMG_MUST_HEIGHT, C.THRESHOLD_IMG_MUST_WIDTH)  # img assertion

    # *** Step 4 *** refine results:
    # refine img according to size -> OCR text area filter
    # ignore too large and highly likely text areas
    corners_img = det.img_refine(org, corners_img,
                                 C.THRESHOLD_IMG_MAX_HEIGHT_RATIO,                      # ignore too large imgs
                                 C.THRESHOLD_TEXT_EDGE_RATIO, C.THRESHOLD_TEXT_HEIGHT)  # ignore text areas
    # merge overlapped corners, and remove nested corners
    # corners_img = det.merge_corners(corners_img)
    # remove text
    corners_block = det.rm_text(org, corners_block,
                                C.THRESHOLD_IMG_MUST_HEIGHT, C.THRESHOLD_IMG_MUST_WIDTH,  # img assertion
                                C.OCR_PADDING, C.OCR_MIN_WORD_AREA)                       # ignore text area
    corners_img = det.rm_text(org, corners_img,
                                C.THRESHOLD_IMG_MUST_HEIGHT, C.THRESHOLD_IMG_MUST_WIDTH,    # img assertion
                                C.OCR_PADDING, C.OCR_MIN_WORD_AREA)                         # ignore text area
    corners_compo = det.rm_text(org, corners_compo,
                                C.THRESHOLD_IMG_MUST_HEIGHT, C.THRESHOLD_IMG_MUST_WIDTH,  # img assertion
                                C.OCR_PADDING, C.OCR_MIN_WORD_AREA)                       # ignore text area

    # *** Step 5 *** classification:
    if is_classify:
        CNN.load()
        compos = seg.clipping(org, corners_compo)
        compos_classes = CNN.predict(compos)
    else:
        compos_classes = None

    # *** Step 6 *** post-processing:
    # remove img elements from original image and segment into smaller size
    img_clean = draw.draw_bounding_box(corners_img, org, color=(255, 255, 255), line=-1)
    seg.segment_img(img_clean, 600, 'output/segment')
    # draw results
    draw_bounding = draw.draw_bounding_box_class(corners_block, org, ['block' for i in range(len(corners_block))], C.COLOR)
    draw_bounding = draw.draw_bounding_box_class(corners_img, draw_bounding, ['img' for j in range(len(corners_img))], C.COLOR)
    draw_bounding = draw.draw_bounding_box_class(corners_compo, draw_bounding, compos_classes, C.COLOR)
    draw_boundary = draw.draw_boundary(boundary_rec, org.shape)
    # save results
    if is_save:
        cv2.imwrite('output/b.png', draw_boundary)
        cv2.imwrite(out_img_draw, draw_bounding)
        cv2.imwrite(out_img_gradient, binary)
        cv2.imwrite(out_img_clean, img_clean)
        file.save_corners(out_label, corners_block, 'div')
        file.save_corners(out_label, corners_img, 'img', False)

    end = file.timer(start)
    print('Save ' + index + '\n')
