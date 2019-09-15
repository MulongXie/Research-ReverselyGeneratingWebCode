import glob
from os.path import join as pjoin, exists

import ocr
import ui
import merge
from file_utils import time_start, timer_end
from CONFIG_UIED import Config

is_ctpn = True
is_uied = True
is_merge = True

is_clip = True
C = Config()
C.build_output_folders(is_clip)

start_index = 0
end_index = 2000

input_paths_img = glob.glob(pjoin(C.ROOT_INPUT, '*.png'))
input_paths_img = sorted(input_paths_img, key=lambda x: int(x.split('\\')[-1][:-4]))  # sorted by index
for input_path_img in input_paths_img:
    index = input_path_img.split('\\')[-1][:-4]
    if int(index) < start_index:
        continue
    if int(index) > end_index:
        break

    start = time_start()

    label_compo = pjoin(C.ROOT_LABEL_UIED, index + '.json')
    img_uied_drawn =pjoin(C.ROOT_IMG_DRAWN_UIED, index + '.png')
    img_uied_grad = pjoin(C.ROOT_IMG_GRADIENT_UIED, index + '.png')
    label_text = pjoin(C.ROOT_LABEL_CTPN, index + '.txt')
    img_ctpn_drawn = pjoin(C.ROOT_IMG_DRAWN_CTPN, index + '.png')
    img_merge = pjoin(C.ROOT_IMG_MERGE, index + '.png')

    try:
        if is_ctpn:
            ocr.ctpn(input_path_img, label_text, img_ctpn_drawn)
        if is_uied:
            ui.uied(input_path_img, label_compo, img_uied_drawn, img_uied_grad)
        if is_merge:
            merge.incorporate(input_path_img, label_compo, label_text, img_merge, is_clip)
    except:
        print("Bad Img")

    end = timer_end(start)
