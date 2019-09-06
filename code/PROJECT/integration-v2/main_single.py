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

start = time.clock()
# initialization
C = Config()
CNN = CNN()
CNN.load()
is_merge_nested = False
is_shrink_img = False
is_img_inspect = True
is_save = True
is_clip = False


def pre_processing():
    # *** Step 1 *** pre-processing: gray, gradient, binary
    org, gray = pre.read_img('input/dribbble/x.png', (0, 3000))  # cut out partial img
    binary = pre.preprocess(gray, 3)
    return org, binary


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

        draw.draw_bounding_box(org, corners_compo, show=True)

        # *** Step 4 *** classification: clip and classify the components candidates -> ignore noises -> refine img
        compos = seg.clipping(org, corners_compo)
        compos_class = CNN.predict(compos)
        corners_compo, compos_class = det.compo_filter(org, corners_compo, compos_class)
        corners_compo, compos_class = det.strip_img(corners_compo, compos_class, corners_img)

        draw.draw_bounding_box(org, corners_compo, show=True)

        # *** Step 5 *** result refinement
        if is_merge_nested:
            corners_img, _ = det.merge_corner(corners_img, ['img' for i in range(len(corners_img))])
            corners_compo, compos_class = det.merge_corner(corners_compo, compos_class)
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
            det.compo_in_img(processing, org, binary, corners_img, corners_block, corners_compo, compos_class)

        return corners_block, corners_img, corners_compo, compos_class, corners_text

    # *** used for img inspection ***
    # only consider rectangular components
    else:
        boundary_rec, boundary_non_rec = det.boundary_detection(binary, min_rec_evenness=C.THRESHOLD_REC_MIN_EVENNESS_STRONG)
        corners_rec = det.get_corner(boundary_rec)
        corners_block, corners_img, corners_compo = det.block_or_compo(org, binary, corners_rec)

        compos = seg.clipping(org, corners_compo)
        compos_class = CNN.predict(compos)

        corners_compo, compos_class = det.compo_filter(org, corners_compo, compos_class)
        corners_compo, compos_class = det.strip_img(corners_compo, compos_class, corners_img)
        corners_block, _ = det.rm_text(org, corners_block, ['block' for i in range(len(corners_block))])
        corners_compo, compos_class = det.rm_text(org, corners_compo, compos_class)

        return corners_block, corners_compo, compos_class


def post_processing(org, binary, corners_block, corners_img, corners_compo, compos_class, corners_text):
    # *** Step 7 *** post-processing: remove img elements from original image and segment into smaller size
    # draw results
    draw_bounding = draw.draw_bounding_box_class(org, corners_compo, compos_class)
    draw_bounding = draw.draw_bounding_box_class(draw_bounding, corners_block, ['block' for i in range(len(corners_block))])
    draw_bounding = draw.draw_bounding_box_class(draw_bounding, corners_img, ['img' for i in range(len(corners_img))])
    draw_bounding = draw.draw_bounding_box(draw_bounding, corners_text, line=1)
    # save results
    if is_save:
        binary_r = pre.reverse_binary(binary)
        cv2.imwrite('output/org.png', org)
        cv2.imwrite('output/gradient_r.png', binary_r)
        cv2.imwrite('output/gradient.png', binary)
        cv2.imwrite('output/labeled.png', draw_bounding)
        file.save_corners_json('output/compo.json', corners_block, ['div' for i in range(len(corners_block))])
        file.save_corners_json('output/compo.json', corners_img, ['div' for i in range(len(corners_img))])
        file.save_corners_json('output/compo.json', corners_compo, compos_class)
    if is_clip:
        file.save_clipping(org, 'output/clip', corners_block, ['div' for k in range(len(corners_block))])
        file.save_clipping(org, 'output/clip', corners_img, ['div' for k in range(len(corners_img))])
        file.save_clipping(org, 'output/clip', corners_compo, compos_class)


def _main():
    org, binary = pre_processing()
    corners_block, corners_img, corners_compo, compos_class, corners_text = processing(org, binary)
    post_processing(org, binary, corners_block, corners_img, corners_compo, compos_class, corners_text)

    file.timer(start)


if __name__ == '__main__':
    _main()


