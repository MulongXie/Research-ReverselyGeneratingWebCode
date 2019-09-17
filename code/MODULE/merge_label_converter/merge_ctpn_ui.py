import glob
from os.path import join as pjoin

import merge

img_section = (1500, 1500)  # selected img section, height and width

img_root = "E:\Mulong\Datasets\dataset_webpage\page10000\org"
label_root = "E:\Mulong\Datasets\dataset_webpage\page10000\\relabel"

ctpn_root = 'C:\\Users\\Shae\\Desktop\\label\\ctpn'
uied_root = 'C:\\Users\\Shae\\Desktop\\label\\uied'
merge_root = 'C:\\Users\\Shae\\Desktop\\label\\merge'
drawn_root = 'C:\\Users\\Shae\\Desktop\\label\\drawn'

ctpn_paths = glob.glob(pjoin(ctpn_root, '*.txt'))
ctpn_paths = sorted(ctpn_paths, key=lambda x: int(x.split('\\')[-1][:-4]))  # sorted by index
for ctpn_path in ctpn_paths:
    index = ctpn_path.split('\\')[-1][:-4]
    img_path = pjoin(img_root, index + '.png')
    uied_path = pjoin(uied_root, index + '.json')

    drawn_path = pjoin(drawn_root, index + '.png')
    merge_path = pjoin(merge_root, index + '.json')

    merge.incorporate(img_path, uied_path, ctpn_path, drawn_path, merge_path, img_section)
