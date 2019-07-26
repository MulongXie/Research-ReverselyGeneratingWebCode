from CONFIG import Config

from os.path import join as pyjoin
import glob

C = Config()
input_root = C.ROOT_IMG_ORG

input_paths = glob.glob(pyjoin(input_root, '*.png'))

input_paths = sorted(input_paths, key=lambda x: int(x.split('\\')[-1][:-4]))

start_index = 10
end_index = 10

for input_path in input_paths:
    index = input_path.split('\\')[-1][:-4]
    if int(index) < start_index:
        continue
    if int(index) > end_index:
        break

    print(input_path)