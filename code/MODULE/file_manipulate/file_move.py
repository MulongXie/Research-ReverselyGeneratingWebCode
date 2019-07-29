import os
import shutil
import glob

src = 'D:\datasets\dataset_webpage\data\img_segment\img'
dest = 'E:\Mulong\Datasets\dataset_webpage\org'

# for l in os.listdir(src):
#     # shutil.copy(os.path.join(img_root, (l + '/org.png')), os.path.join(input_root, (l + '.png')))
#     print(l)

for g in glob.glob(src + '/*/org.png'):
    print(g)
    shutil.copy(g, os.path.join(dest, g.split('\\')[-2] + '.png'))