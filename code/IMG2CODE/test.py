import glob
from os.path import join as pyjoin

import ocr
from CONFIG import Config
C = Config()

input_root = C.ROOT_INPUT
input_paths = glob.glob(pyjoin(input_root, '*.png'))
input_paths = sorted(input_paths, key=lambda x: int(x.split('\\')[-1][:-4]))  # sorted by index

start_index = 1
end_index = 100

for input_path in input_paths:
    index = input_path.split('\\')[-1][:-4]
    if int(index) < start_index:
        continue
    if int(index) > end_index:
        break

    print(input_path)
    ocr.ctpn(input_path, )