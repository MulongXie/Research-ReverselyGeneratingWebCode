import body
import ip_preprocessing as pre
import ip_draw as draw
import file_utils as file
from CONFIG_UIED import Config

import cv2
import time

start = time.clock()
# initialization
C = Config()
model = 'cnn'

if model == 'cnn':
    from MODEL_CNN import CNN
    clf = CNN()
    clf.load()
elif model == 'svm':
    from MODEL_SVM import SVM
    clf = SVM()
    clf.load()


def save(org, binary, corners_block, corners_img, corners_compo, compos_class, output_path_label, output_path_img_drawn, output_path_img_bin):
    # *** Step 7 *** post-processing: remove img elements from original image and segment into smaller size
    # draw results
    draw_bounding = draw.draw_bounding_box_class(org, corners_compo, compos_class)
    draw_bounding = draw.draw_bounding_box_class(draw_bounding, corners_block, ['div' for i in range(len(corners_block))])
    draw_bounding = draw.draw_bounding_box_class(draw_bounding, corners_img, ['img' for i in range(len(corners_img))])
    # save results
    binary_r = pre.reverse_binary(binary)
    cv2.imwrite('data/output/org.png', org)
    cv2.imwrite('data/output/gradient_r.png', binary_r)
    cv2.imwrite(output_path_img_bin, binary)
    cv2.imwrite(output_path_img_drawn, draw_bounding)
    file.save_corners_json(output_path_label, corners_block, ['div' for i in range(len(corners_block))], new=True)
    file.save_corners_json(output_path_label, corners_img, ['img' for i in range(len(corners_img))], new=False)
    file.save_corners_json(output_path_label, corners_compo, compos_class, new=False)


def uied(input_path_img, output_path_label, output_path_img_drawn, output_path_img_bin, img_section):
    print('UIED for', input_path_img)
    org, binary = body.pre_processing(input_path_img, img_section)
    corners_block, corners_img, corners_compo, compos_class = body.processing(org, binary, clf)
    save(org, binary, corners_block, corners_img, corners_compo, compos_class, output_path_label, output_path_img_drawn, output_path_img_bin)
    print('*** UI Detection Complete ***')



