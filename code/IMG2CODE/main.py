import glob
from os.path import join as pjoin

import ocr
import ui
import merge
from file_utils import time_start, timer_end
from CONFIG import Config

C = Config()
input_root_img = C.ROOT_INPUT
output_root = C.ROOT_OUTPUT

is_ctpn = True
is_uied = False
is_merge = False

start_index = 100
end_index = 150

input_paths_img = glob.glob(pjoin(input_root_img, '*.png'))
input_paths_img = sorted(input_paths_img, key=lambda x: int(x.split('\\')[-1][:-4]))  # sorted by index
for input_path_img in input_paths_img:
    index = input_path_img.split('\\')[-1][:-4]
    if int(index) < start_index:
        continue
    if int(index) > end_index:
        break

    start = time_start()

    label_compo = pjoin(output_root, 'ip_label', index + '.json')
    label_text = pjoin(output_root, 'ctpn_label', index + '.txt')
    img_ctpn_drawn = pjoin(output_root, 'ctpn_drawn', index + '.png')
    img_uied_drawn =pjoin(output_root, 'ip_drawn', index + '.png')
    img_uied_bin = pjoin(output_root, 'ip_img_gradient', index + '.png')
    img_merge = pjoin(output_root, 'ctpn_merge', index + '.png')

    if is_ctpn:
        ocr.ctpn(input_path_img, label_text, img_ctpn_drawn)
    if is_uied:
        ui.uied(input_path_img, label_compo, img_uied_drawn, img_uied_bin)
    if is_merge:
        merge.incorporate(input_path_img, label_compo, label_text, img_merge)

    end = timer_end(start)
