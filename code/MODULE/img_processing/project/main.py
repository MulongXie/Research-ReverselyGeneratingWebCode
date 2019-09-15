import body
import ip_preprocessing as pre
import ip_draw as draw
import file_utils as file
from CONFIG import Config
from MODEL import CNN

import cv2
import time
import glob
from os.path import join as pyjoin

# initialization
C = Config()
C.build_output_folders(False)
input_root = C.ROOT_INPUT
input_paths = glob.glob(pyjoin(input_root, '*.png'))
input_paths = sorted(input_paths, key=lambda x: int(x.split('\\')[-1][:-4]))  # sorted by index


def save(index, org, binary, corners_block, corners_img, corners_compo, compos_class, corners_text):

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
    cv2.imwrite(out_img_gradient, binary)
    cv2.imwrite(out_img_draw, draw_bounding)
    cv2.imwrite(out_img_clean, img_clean)
    file.save_corners_json(out_label, corners_block, ['div' for i in range(len(corners_block))])
    file.save_corners_json(out_label, corners_img, ['div' for i in range(len(corners_img))])
    file.save_corners_json(out_label, corners_compo, compos_class)


def _main():
    # start image and end image
    start_index = 1
    end_index = 20

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
            org, binary = body.pre_processing(input_path)
            corners_block, corners_img, corners_compo, compos_class, corners_text = body.processing(org, binary)
            save(index, org, binary, corners_block, corners_img, corners_compo, compos_class, corners_text)
        except:
            print('Bad Input', index + '\n')
            continue

        file.timer(start)
        print('Save ' + index + '\n')


if __name__ == '__main__':
    _main()
