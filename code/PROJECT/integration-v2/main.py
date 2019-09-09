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
import glob
from os.path import join as pyjoin

# choose functionality
is_shrink_img = False
is_img_inspect = True
is_save = True

# initialization
C = Config()
C.build_output_folders(False)
input_root = C.ROOT_INPUT
input_paths = glob.glob(pyjoin(input_root, '*.png'))
input_paths = sorted(input_paths, key=lambda x: int(x.split('\\')[-1][:-4]))  # sorted by index
CNN = CNN()
CNN.load()


def pre_processing(img):
    # *** Step 1 *** pre-processing: gray, gradient, binary
    org, gray = pre.read_img(img, (0, 3000))  # cut out partial img
    binary = pre.preprocess(gray, 1)
    return org, binary


# set timeout
def processing(org, binary, main=True):
    if main:
        # *** Step 2 *** object detection: get connected areas -> get boundary -> get corners
        boundary_rec, boundary_non_rec = det.boundary_detection(binary)
        corners_rec = det.get_corner(boundary_rec)
        corners_non_rec = det.get_corner(boundary_non_rec)

        # *** Step 3 *** data processing: identify blocks and compos from rectangles -> identify irregular compos
        corners_block, corners_img, corners_compo = det.block_or_compo(org, binary, corners_rec)
        det.compo_irregular(org, corners_non_rec, corners_img, corners_compo)
        corners_img, _ = det.rm_text(org, corners_img, ['img' for i in range(len(corners_img))])

        # *** Step 4 *** classification: clip and classify the components candidates -> ignore noises -> refine img
        compos = seg.clipping(org, corners_compo)
        compos_class = CNN.predict(compos)
        corners_compo, compos_class = det.compo_filter(org, corners_compo, compos_class)
        corners_compo, compos_class = det.strip_img(corners_compo, compos_class, corners_img)

        # *** Step 5 *** result refinement
        corners_img, _ = det.merge_corner(corners_img, ['img' for i in range(len(corners_img))])
        corners_block, _ = det.rm_text(org, corners_block, ['block' for i in range(len(corners_block))])
        corners_img, _ = det.rm_text(org, corners_img, ['img' for i in range(len(corners_img))])
        corners_compo, compos_class = det.rm_text(org, corners_compo, compos_class)
        if is_shrink_img:
            corners_img = det.img_shrink(org, binary, corners_img)

        # *** Step 6 *** text detection from cleaned image
        img_clean = draw.draw_bounding_box(org, corners_img, color=(255, 255, 255), line=-1)
        corners_word = ocr.text_detection(org, img_clean)
        corners_text = ocr.text_merge_word_into_line(org, corners_word)

        # *** Step 7 *** img inspection: search components in img element
        if is_img_inspect:
            corners_block, corners_img, corners_compo, compos_class = det.compo_in_img(processing, org, binary, corners_img, corners_block, corners_compo, compos_class)

        return corners_block, corners_img, corners_compo, compos_class, corners_text

    # *** used for img inspection ***
    # only consider rectangular components
    else:
        boundary_rec, boundary_non_rec = det.boundary_detection(binary, min_rec_evenness=C.THRESHOLD_REC_MIN_EVENNESS_STRONG, show=False)
        corners_rec = det.get_corner(boundary_rec)
        corners_block, corners_img, corners_compo = det.block_or_compo(org, binary, corners_rec)

        compos = seg.clipping(org, corners_compo)
        compos_class = CNN.predict(compos)
        corners_compo, compos_class = det.compo_filter(org, corners_compo, compos_class)
        corners_compo, compos_class = det.strip_img(corners_compo, compos_class, corners_img)

        corners_block, _ = det.rm_text(org, corners_block, ['block' for i in range(len(corners_block))])
        corners_compo, compos_class = det.rm_text(org, corners_compo, compos_class)

        return corners_block, corners_compo, compos_class


def post_processing(index, org, binary, corners_block, corners_img, corners_compo, compos_class, corners_text):

    out_img_gradient = pyjoin(C.ROOT_IMG_GRADIENT, index + '.png')
    out_img_draw = pyjoin(C.ROOT_IMG_DRAWN, index + '.png')
    out_img_clean = pyjoin(C.ROOT_IMG_CLEAN, index + '.png')
    out_label = pyjoin(C.ROOT_LABEL, index + '.json')

    # *** Step 7 *** post-processing: remove img elements from original image and segment into smaller size
    img_clean = draw.draw_bounding_box(org, corners_img, color=(255, 255, 255), line=-1)
    # draw results
    draw_bounding = draw.draw_bounding_box_class(org, corners_compo, compos_class)
    draw_bounding = draw.draw_bounding_box_class(draw_bounding, corners_block, ['block' for i in range(len(corners_block))])
    draw_bounding = draw.draw_bounding_box_class(draw_bounding, corners_img, ['img' for i in range(len(corners_img))])
    draw_bounding = draw.draw_bounding_box(draw_bounding, corners_text, line=1)
    # save results
    if is_save:
        cv2.imwrite(out_img_gradient, binary)
        cv2.imwrite(out_img_draw, draw_bounding)
        cv2.imwrite(out_img_clean, img_clean)
        file.save_corners_json(out_label, corners_block, ['div' for i in range(len(corners_block))])
        file.save_corners_json(out_label, corners_img, ['div' for i in range(len(corners_img))])
        file.save_corners_json(out_label, corners_compo, compos_class)


def _main():
    # start image and end image
    start_index = 207
    end_index = 700

    for input_path in input_paths:
        index = input_path.split('\\')[-1][:-4]
        if int(index) < start_index:
            continue
        if int(index) > end_index:
            break

        start = time.clock()
        print(input_path)
        print(time.ctime())

        try:
            org, binary = pre_processing(input_path)
            corners_block, corners_img, corners_compo, compos_class, corners_text = processing(org, binary)
            post_processing(index, org, binary, corners_block, corners_img, corners_compo, compos_class, corners_text)
        except:
            print('Bad Input', index + '\n')
            continue

        file.timer(start)
        print('Save ' + index + '\n')


if __name__ == '__main__':
    _main()
