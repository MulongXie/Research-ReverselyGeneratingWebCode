import os
from os.path import join as pjoin
import glob
import json
import pandas as pd
import numpy as np


def segment_label(segment_size, label, output_path):
    def extent(item, index, segment_label, segment_size):
        # calculate the extent segment
        extent_item = item.copy()
        extent_item['row_min'] = 0
        extent_item['height'] = item['height'] - (segment_size - item['row_min'] - 1)
        extent_item['segment_no'] = item['segment_no'] + 1

        # revise the org large segment
        item['height'] = segment_size - item['row_min'] - 1

        # append the new items
        item['row_max'] = item['row_min'] + item['height']
        segment_label.loc[index] = item

        # extent recursively until the size is smaller than the segment size
        if (extent_item['row_min'] + extent_item['height']) >= segment_size:
            index = extent(extent_item, index + 1, segment_label, segment_size)
        else:
            index += 1
            extent_item['row_max'] = extent_item['row_min'] + extent_item['height']
            segment_label.loc[index] = extent_item

        return index

    # initialize the segment labels by adding segment_no column and changing the relative label coordinate
    colums = label.columns.values
    colums = np.append(colums, ['segment_no'])
    segment_label = pd.DataFrame(columns=colums)

    index = 0
    for i in range(len(label)):
        item = label.iloc[i].copy()
        segment_no = int(item['row_min'] / segment_size)
        item['row_min'] = item['row_min'] % segment_size
        item['segment_no'] = segment_no

        # for those excess the segment size range
        if (item['row_min'] + item['height']) >= segment_size:
            index = extent(item, index, segment_label, segment_size)
        else:
            item['row_max'] = item['row_min'] + item['height']
            segment_label.loc[index] = item

        index += 1

    segment_label.to_csv(output_path)


start_index = 1 
end_index = 10
merge_root_csv = 'C:\\Users\\Shae\\Desktop\\label\\merge_csv'

label_paths = glob.glob(pjoin(merge_root_csv, '*.csv'))
label_paths = sorted(label_paths, key=lambda x: int(x.split('\\')[-1][:-4]))  # sorted by index
for label_path in label_paths:
    index = label_path.split('\\')[-1][:-4]
    if int(index) < start_index:
        continue
    if int(index) > end_index:
        break

    print(label_path)
    compos = pd.read_csv(label_path, index_col=0)
    segment_label(600, compos, label_path)
