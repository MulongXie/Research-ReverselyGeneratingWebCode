import cv2
import pandas as pd
from os.path import join as pjoin
import glob

color = {'div': (0, 255, 0), 'img': (0, 0, 255), 'icon': (255, 166, 166), 'input': (255, 166, 0),
                      'text': (77, 77, 255), 'search': (255, 0, 166), 'list': (166, 0, 255), 'select': (166, 166, 166),
                      'button': (0, 166, 255)}


def draw_bounding_box_class(org, corners, compo_class, color_map=color, line=3, show=False, name='img'):
    board = org.copy()
    for i in range(len(corners)):
        board = cv2.rectangle(board, (corners[i][0], corners[i][1]), (corners[i][2], corners[i][3]), color_map[compo_class[i]], line)
        board = cv2.putText(board, compo_class[i], (corners[i][0]+5, corners[i][1]+20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_map[compo_class[i]], 2)
    if show:
        cv2.imshow(name, board)
    return board


def check_label():
    start_index = 4
    end_index = 4

    seg_root = 'E:/Mulong/Datasets/dataset_webpage/page10000/org_segment/'
    label_root = 'C:/Users/Shae/Desktop/label/merge_csv'

    label_paths = glob.glob(pjoin(label_root, '*.csv'))
    label_paths = sorted(label_paths, key=lambda x: int(x.split('\\')[-1][:-4]))  # sorted by index
    for label_path in label_paths:
        index = label_path.split('\\')[-1][:-4]
        if int(index) < start_index:
            continue
        if int(index) > end_index:
            break

        label = pd.read_csv(label_path, index_col=0)
        seg_path = pjoin(seg_root, index)
        for i in range(len(label)):
            compo = label.iloc[i]
            seg_no = label.iloc[i]['segment_no']
            img = cv2.imread(pjoin(seg_path, str(seg_no) + '.png'))

            corner = [compo['column_min'], compo['row_min'], compo['column_max'], compo['row_max']]
            compo_class = compo['class']
            if compo_class != 'text':
                draw_bounding_box_class(img, [corner], [compo_class], show=True)
                k = cv2.waitKey(100)

            # if k == ord('d'):
            #     break
            # elif k == ord('t'):
            #     return



check_label()
