import multiprocessing
import glob
import time
import json
from tqdm import tqdm
from os.path import join as pjoin, exists

import ip_region_proposal as ip
from CONFIG import Config

if __name__ == '__main__':
    # initialization
    C = Config()
    resize_by_height = 800
    input_root = C.ROOT_INPUT
    output_root = C.ROOT_OUTPUT

    # set input root directory and sort all images by their indices
    data = json.load(open('E:\\Mulong\\Datasets\\rico\\instances_train.json', 'r'))
    input_paths_img = [pjoin(input_root, img['file_name'].split('/')[-1]) for img in data['images']]
    input_paths_img = sorted(input_paths_img, key=lambda x: int(x.split('\\')[-1][:-4]))  # sorted by index

    # set the range of target inputs' indices
    num = 0
    start_index = 0  # 61728
    end_index = 1000
    for input_path_img in input_paths_img:
        index = input_path_img.split('\\')[-1][:-4]
        if int(index) < start_index:
            continue
        if int(index) > end_index:
            break

        ip.block_detection(input_path_img, output_root, num, resize_by_height=resize_by_height, show=True)
        num += 1
