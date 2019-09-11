import body
import ip_preprocessing as pre
import ip_draw as draw
import file_utils as file
from CONFIG import Config
from MODEL import CNN

import cv2
import time

start = time.clock()
# initialization
C = Config()
is_clip = True


def save(org, output_path_label, binary, corners_block, corners_img, corners_compo, compos_class, corners_text):
    # *** Step 7 *** post-processing: remove img elements from original image and segment into smaller size
    # draw results
    draw_bounding = draw.draw_bounding_box_class(org, corners_compo, compos_class)
    draw_bounding = draw.draw_bounding_box_class(draw_bounding, corners_block, ['block' for i in range(len(corners_block))])
    draw_bounding = draw.draw_bounding_box_class(draw_bounding, corners_img, ['img' for i in range(len(corners_img))])
    draw_bounding = draw.draw_bounding_box(draw_bounding, corners_text, line=1)
    # save results
    binary_r = pre.reverse_binary(binary)
    cv2.imwrite('data/output/org.png', org)
    cv2.imwrite('data/output/gradient_r.png', binary_r)
    cv2.imwrite('data/output/gradient.png', binary)
    cv2.imwrite('data/output/labeled.png', draw_bounding)
    file.save_corners_json(output_path_label, corners_block, ['div' for i in range(len(corners_block))])
    file.save_corners_json(output_path_label, corners_img, ['img' for i in range(len(corners_img))])
    file.save_corners_json(output_path_label, corners_compo, compos_class)


def uied(input_path_img, output_path_label):
    org, binary = body.pre_processing(input_path_img)
    corners_block, corners_img, corners_compo, compos_class, corners_text = body.processing(org, binary, CNN)
    save(org, output_path_label, binary, corners_block, corners_img, corners_compo, compos_class, corners_text)
    print('*** UI Elements Complete ***')



