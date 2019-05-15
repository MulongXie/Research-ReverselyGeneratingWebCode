import cv2
import numpy as np
import os
import pandas as pd

import img_drawLabel as draw


# cut the original img into fixed-size segment img
def segment_img(segment_size, img_index=0, img_root_path="D:\datasets\dataset_webpage\data\img_segment\img", show=True):
    img_path = os.path.join(img_root_path, str(img_index))
    img_input_path = os.path.join(img_path, 'org.png')
    img_output_path = os.path.join(img_path, 'segment')

    img = cv2.imread(img_input_path)
    height_bottom = np.shape(img)[0]

    h = 0
    segment_no = 0
    while h < height_bottom:
        segment_range = {}
        segment_range['top'] = h
        segment_range['bottom'] = h + segment_size if h + segment_size <= height_bottom else height_bottom
        segment_img = img[segment_range['top']:segment_range['bottom'], :, :]
        cv2.imwrite(os.path.join(img_output_path, str(segment_no) + '.png'), segment_img)

        h += segment_size
        segment_no += 1

        if show:
            cv2.imshow('img', segment_img)
            cv2.waitKey(0)


# extent labels that excess the segment size to the next segment
def segment_extent(item, index, segment_label, segment_size):
    # calculate the extent segment
    extent_item = item.copy()
    extent_item['by'] = 0
    extent_item['bh'] = item['bh'] - (segment_size - item['by'] - 1)
    extent_item['segment_no'] = item['segment_no'] + 1

    # revise the org large segment
    item['bh'] = segment_size - item['by'] - 1

    # append the new items
    segment_label.loc[index] = item

    # extent recursively until the size is smaller than the segment size
    if (extent_item['by'] + extent_item['bh']) >= segment_size:
        index = extent_item(extent_item, index + 1, segment_label, segment_size)
    else:
        index += 1
        segment_label.loc[index] = extent_item

    return index


# change the coordinates and size of labels to fit the img segment
def segment_label(segment_size, label_index=0, label_root_path="D:\datasets\dataset_webpage\data\segment\label"):
    label_path = os.path.join(label_root_path, str(label_index))
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
            index = segment_extent(item, index, segment_label, segment_size)
        else:
            segment_label.loc[index] = item

        index += 1

    segment_label.to_csv(segment_label_path)


# draw label on the segment images
def segment_draw(img_root_path, label_root_path, index=0, show=True):

    img_path = os.path.join(img_root_path, str(index))
    input_path = os.path.join(img_path, 'segment')
    output_path = os.path.join(img_path, 'labeled')
    label_path = os.path.join(label_root_path, str(index) + '\\segment.csv')

    label = pd.read_csv(label_path)

    for s in range(label.iloc[-1].segment_no + 1):
        seg_input_path = os.path.join(input_path, str(s) + '.png')
        seg_output_path = os.path.join(output_path, str(s) + '.png')
        seg_img = cv2.imread(seg_input_path)
        seg_label = label[label['segment_no'] == s]

        draw.label(seg_label, seg_img, seg_output_path, show)


def segment(root_path, index):
    img_root_path = os.path.join(root_path, 'img')
    label_root_path = os.path.join(root_path, 'label')

    # segment the image and corresponding label
    segment_size = 600
    segment_img(segment_size, index, img_root_path)
    segment_label(segment_size, index, label_root_path)

    # draw labels on segments
    segment_draw(img_root_path, label_root_path, index)