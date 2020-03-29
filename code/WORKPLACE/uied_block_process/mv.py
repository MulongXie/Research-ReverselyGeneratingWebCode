import shutil
from glob import glob
from os.path import join as pjoin

src_root = 'E:\\Temp\\rico-block\\'
dest_root = 'E:\\Temp\\rico-block-json\\'

for src_path in glob(pjoin(src_root, '*.json')):
    dest_path = src_path.replace('rico-block', 'rico-block-json')
    shutil.copy(src_path, dest_path)