import cv2
import os
import pandas as pd
import numpy as np

ix, iy = -1, -1
# global variables for visualisation
gb_img = None  # record the new label
gb_label = None  # label of this web page
gb_label_index = None  # index of the new line of label
gb_newlabelnum = 0


def add_label(label, ix, iy, x, y, segment_no):
    l = {'bx': ix, 'by': iy, 'bh': int(y - iy), 'bw': int(x - ix), 'segment_no': segment_no}
    label = label.append(l, ignore_index=True)
    print('... Number of New Labels: %d ...' % gb_newlabelnum)
    return label


def overlap(bottom, top, board):
    cv2.addWeighted(bottom, 0.7, top, 0.3, 0, board)
    cv2.imshow('segment', board)


def draw_label(label, img):
    for i in range(len(label)):
        l = label.iloc[i]
        cv2.rectangle(img, (int(l['bx']), int(l['by'])), (int(l['bx'] + l['bw']), int(l['by'] + l['bh'])), (0, 0, 255), 1)
    cv2.imshow('img', img)


def relabel(event, x, y, flags, param):
    global ix, iy, gb_img, gb_label, gb_label_index, gb_newlabelnum
    seg_index = param[0]

    if event == cv2.EVENT_LBUTTONDOWN:
        # fetch the start points
        ix, iy = x, y
        gb_img_pre = gb_img.copy()
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        # draw the rectangle
        img = gb_img.copy()
        cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 1)
        cv2.imshow('img', img)
    elif event == cv2.EVENT_LBUTTONUP:
        # save the labeled area
        gb_label_index += 1
        gb_newlabelnum += 1
        gb_label = add_label(gb_label, ix, iy, x, y, seg_index)
        draw_label(gb_label, gb_img)


def add_tips(flag):
    img = np.zeros((150, 400, 3), dtype=np.uint8)
    font_scale = 0.5
    color = (255, 255, 255)
    thick = 1
    # webpage-level
    if flag == 0:
        cv2.putText(img, 'a: Go Previous Image', (0, 20), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thick)
        cv2.putText(img, 'd: Go Next Image', (0, 40), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thick)
        cv2.putText(img, 's: Start Relabelling', (0, 60), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thick)
        cv2.putText(img, 'q: Go Next WebPage & Discard Label', (0, 100), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thick)
        cv2.putText(img, 'r: Remove Labels of This Image', (0, 120), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thick)
        cv2.putText(img, 'n: Terminate Program', (0, 140), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thick)
    # segment-level
    elif flag == 1:
        cv2.putText(img, 'd: Quit Relabelling Mode', (0, 20), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thick)
        cv2.putText(img, 'z: Delete the Last Label', (0, 40), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thick)
    cv2.imshow('tips', img)
    cv2.moveWindow('tips', 2000, 0)


def view_data(start_point, data_position='D:\datasets\dataset_webpage\data'):
    # *** step 1 *** Root Path
    # retrieve global variables for relabel
    global gb_img, gb_label, gb_label_index, gb_newlabelnum
    # set root path
    root = os.path.join(data_position, 'img_segment')
    img_root = os.path.join(root, 'img')
    label_root = os.path.join(root, 'label')
    relabel_root = os.path.join(root, 'label_refine')  # relabels path

    # *** step 2 *** Iterate Web Pages
    # iterate all web pages from the start point
    indices = sorted([int(l[:-4]) for l in os.listdir(label_root)])
    for index in indices[indices.index(start_point):]:
        # set paths
        img_path = os.path.join(os.path.join(img_root, str(index)), 'segment')
        label_path = os.path.join(label_root, str(index) + '.csv')
        relabel_path = os.path.join(relabel_root, str(index) + '.csv')
        # read paths of images
        seg_img_paths = []
        if os.path.exists(img_path):
            seg_img_paths = [p for p in os.listdir(img_path)]
            seg_img_paths.sort(key=lambda v: int(v[:-4]))  # sort by img index
            seg_img_paths = [os.path.join(img_path, p) for p in seg_img_paths]
        # read existing label
        if os.path.exists(label_path):
            label = pd.read_csv(label_path, index_col=0)
            label_new = label.drop(index=label.index.values)
            gb_newlabelnum = 0

        print("\n*** Start Checking %s ***" % (img_path))
        print("*** Number of Labels: %d ***" % (len(label)))

        # *** step 3 *** Iterate Segment Images
        # iterate all image segments for each web page
        save = True
        move = True
        passed = {}
        s = 0
        while s < len(seg_img_paths):
            if not os.path.exists(seg_img_paths[s]):
                break
            # show tips
            add_tips(0)

            # read segment image
            seg_img = cv2.imread(seg_img_paths[s])
            seg_index = int(seg_img_paths[s].split('\\')[-1][:-4])
            if move:
                if seg_img_paths[s] is not '':
                    print(seg_img_paths[s])
                gb_img = seg_img.copy()
                if str(seg_index) not in passed:
                    gb_label = label[label['segment_no'] == seg_index]
                else:
                    gb_label = label_new[label_new['segment_no'] == seg_index]
                move = False

            # *** step 4 *** Web Page-Level Options
            # draw labels on the segment image
            draw_label(gb_label, gb_img)
            key = cv2.waitKey(0)

            # back to the previous image
            if key == ord('a'):
                s = s - 1 if s >= 1 else 0
                move = True
                continue
            # next image
            elif key == ord('d'):
                s += 1
                move = True
                if str(seg_index) in passed:
                    continue
            # remove all existing labels
            elif key == ord('r'):
                gb_img = seg_img.copy()
                gb_label = gb_label.drop(index=gb_label.index.values)
                label_new = label_new.drop(index=label_new[label_new['segment_no']==seg_index].index.values)
                print('*** Remove Labels of Image %d ***' % seg_index)
            # skip rest segment images and discard the current relabel
            elif key == ord('q'):
                s += 1
                move = True
                print('*** Image is Discarded ***')
                continue
            elif key == ord('e'):
                save = False
                print('*** Next Web Page ***\n')
                break
            # terminate the program
            elif key == ord('n'):
                print('\n*** Program Terminated ***')
                return

            # *** step 5 *** Segment-Level Options
            # enter label mode
            elif key == ord('s'):
                # show tips
                add_tips(1)

                print('------ Revise Labels Start ------')
                gb_label_index = len(gb_label) - 1
                # set mouse callback function
                cv2.setMouseCallback('img', relabel, [seg_index])
                while (1):
                    k = cv2.waitKey(0)
                    # withdraw the last label
                    if k == ord('z'):
                        if gb_label_index >= 0:
                            gb_label = gb_label.drop(index=gb_label.index[gb_label_index])
                            gb_label_index -= 1
                        gb_newlabelnum = gb_newlabelnum - 1 if gb_newlabelnum >= 1 else 0
                        gb_img = seg_img.copy()
                        draw_label(gb_label, gb_img)

                    # quit label mode
                    elif k == ord('d'):
                        print('------ ReLabel End ------')
                        move = True
                        break
            else:
                continue

            cv2.destroyAllWindows()
            label_new = label_new.append(gb_label, ignore_index=True, sort=False)
            passed[str(seg_index)] = 1
            print('... Number of Current Labels: %d ...' % len(label_new))


        if save:
            label_new.to_csv(relabel_path)
            print('*** %d Labels Saved to %s ***\n' % (len(label_new), relabel_path))


view_data(42)