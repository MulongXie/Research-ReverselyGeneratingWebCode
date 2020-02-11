import glob
from os.path import join as pjoin, exists
import time
import json

import ip_region_proposal as ip
from CONFIG import Config

# initialization
is_clip = False
C = Config()
C.build_output_folders(is_clip)
resize_by_height = 800

# set input root directory and sort all images by their indices
data = json.load(open('data/instances_val.json', 'r'))
input_paths_img = [pjoin(C.ROOT_INPUT, img['file_name'].split('/')[-1]) for img in data['images']]
input_paths_img = sorted(input_paths_img, key=lambda x: int(x.split('\\')[-1][:-4]))  # sorted by index
# set the range of target inputs' indices
start_index = 0
end_index = 100000
for input_path_img in input_paths_img:
    index = input_path_img.split('\\')[-1][:-4]
    if int(index) < start_index:
        continue
    if int(index) > end_index:
        break

    # *** start processing ***
    start = time.clock()
    ip.compo_detection(input_path_img, C.ROOT_IP, resize_by_height)
    print('*** Total Time Taken:%.3f s ***' % (time.clock() - start))
    print(time.ctime(), '\n')
