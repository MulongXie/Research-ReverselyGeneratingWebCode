import os
from os.path import join as pjoin
import glob
import json
import pandas as pd

start_index = 1
end_index = 10

merge_root = 'C:\\Users\\Shae\\Desktop\\label\\merge'
merge_root_csv = 'C:\\Users\\Shae\\Desktop\\label\\merge_csv'

label_paths = glob.glob(pjoin(merge_root, '*.json'))
label_paths = sorted(label_paths, key=lambda x: int(x.split('\\')[-1][:-5]))  # sorted by index
for label_path in label_paths:
    index = label_path.split('\\')[-1][:-5]
    if int(index) < start_index:
        continue
    if int(index) > end_index:
        break

    label_f = open(label_path, 'r')
    compos = json.load(label_f)

    df = pd.DataFrame(columns=list(compos['compos'][0].keys()))

    for compo in compos['compos']:
        df = df.append(compo, True)

    df.to_csv(pjoin(merge_root_csv, index + '.csv'))
