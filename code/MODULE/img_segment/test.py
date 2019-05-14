import cv2
import os
import pandas as pd
import numpy as np

import segment_utils as seg


def extent(item, index, segment_label, segment_size):
    # calculate the extent segment
    extent_item = item.copy()
    extent_item['by'] = 0
    extent_item['bh'] = item['bh'] - (segment_size - item['by'] - 1)
    extent_item['segment_no'] = item['segment_no'] + 1

    # revise the org large segment
    item['bh'] = segment_size - item['by'] - 1

    # append the new items
    segment_label.loc[index] = item

    # extent until the size is smaller than the segment size
    if (extent_item['by'] + extent_item['bh']) >= segment_size:
        index = extent_item(extent_item, index + 1, segment_label, segment_size)
    else:
        index += 1
        segment_label.loc[index] = extent_item

    return index


def segment_label(segment_size, label_name=0, label_root_path="D:\datasets\dataset_webpage\data\segment\label"):
    label_path = os.path.join(label_root_path, str(label_name))
    org_label_path = os.path.join(label_path, 'org.csv')
    segment_label_path = os.path.join(label_path, 'segment.csv')

    # read the original label
    org_label = pd.read_csv(org_label_path, index_col=0)

    # initialize the segment labels by adding segment_no column and changing the relative label coordinate
    colums = org_label.columns.values
    colums = np.append(colums, ['segment_no'])
    segment_label = pd.DataFrame(columns=colums)

    index = 0
    for i in range(len(org_label)):
        item = org_label.iloc[i].copy()
        segment_no = int(item['by'] / segment_size)
        item['by'] = item['by'] % segment_size
        item['segment_no'] = segment_no

        # for those excess the segment size range
        if (item['by'] + item['bh']) >= segment_size:
            index = extent(item, index, segment_label, segment_size)
        else:
            segment_label.loc[index] = item

        index += 1

    segment_label.to_csv(segment_label_path)

