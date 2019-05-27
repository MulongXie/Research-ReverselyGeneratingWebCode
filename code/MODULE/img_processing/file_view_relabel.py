import cv2
import os
import pandas as pd

ix, iy = -1, -1
gb_img = None   # original image segment
gb_org = None   # copy of original image segment
gb_label = None  # label of this web page
gb_no = None  # index of the new line of label
gb_newlabel = None


def add_label(label, ix, iy, x, y, segment_no):
    l = {'bx': ix, 'by': iy, 'bh': int(x - ix), 'bw': int(y - iy), 'segment_no': str(segment_no)}
    label = label.append(l, ignore_index=True)
    return label


def relabel(event, x, y, flags, param):
    global ix, iy, gb_img, gb_org, gb_label, gb_no, gb_newlabel
    seg_no = param[0]

    if event == cv2.EVENT_LBUTTONDOWN:
        # fetch the start points
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        # draw the rectangle
        cv2.rectangle(gb_img, (ix, iy), (x, y), (0, 255, 0), -1)
        cv2.addWeighted(gb_org, 0.7, gb_img, 0.3, 0, gb_img)
        cv2.imshow('segment', gb_img)
    elif event == cv2.EVENT_LBUTTONUP:
        # save the labeled area
        gb_no += 1
        gb_newlabel += 1
        gb_label = add_label(gb_label, ix, iy, x, y, seg_no)


def view_data(data_position = 'D:\datasets\dataset_webpage\data'):
    # retrieve global variables for relabel
    global gb_img, gb_org, gb_label, gb_no, gb_newlabel
    # set root path
    root = os.path.join(data_position, 'img_segment')
    img_root = os.path.join(root, 'img')
    label_root = os.path.join(root, 'label')
    relabel_root = os.path.join(root, 'label_refine')

    labels = os.listdir(label_root)
    indices = sorted([int(l[:-4]) for l in labels])

    # iterate all web pages
    for index in indices:
        # set paths
        img_path = os.path.join(img_root, str(index))
        img_path_segment = os.path.join(img_path, 'segment')
        img_path_labeled = os.path.join(img_path, 'labeled')
        label_path = os.path.join(label_root, str(index) + '.csv')
        relabel_path = os.path.join(relabel_root, str(index) + '.csv')

        print("\n*** View Start %s ***" % img_path)

        # read original images, labeled images and labels
        seg_imgs_path = []
        labeled_imgs_path = []
        if os.path.exists(img_path_segment):
            seg_imgs_path = [os.path.join(img_path_segment, p) for p in os.listdir(img_path_segment)]
        if os.path.exists(img_path_labeled):
            labeled_imgs_path = [os.path.join(img_path_labeled, p) for p in os.listdir(img_path_labeled)]
        if os.path.exists(label_path):
            label = pd.read_csv(label_path)
            gb_label = label
            gb_newlabel = 0

        # iterate all image segments
        # show all images to validate labels
        s = 0
        l = 0
        save = False
        while s is not 1000 or l is not 1000 :
            # read and show original image segments
            if s < len(seg_imgs_path) and os.path.exists(seg_imgs_path[s]):
                print(seg_imgs_path[s])
                seg_img = cv2.imread(seg_imgs_path[s])
                seg_img = cv2.resize(seg_img, (1200, 500))
                cv2.imshow('segment', seg_img)
                s += 1
            else:
                s = 1000
            # read and show labeled image segments
            if l < len(labeled_imgs_path) and os.path.exists(labeled_imgs_path[l]):
                print(labeled_imgs_path[l])
                lab_img = cv2.imread(labeled_imgs_path[l])
                lab_img = cv2.resize(lab_img, (1200, 500))
                cv2.imshow('labeled', lab_img)
                l += 1
            else:
                l = 1000
            key = cv2.waitKey(0)

            # back to the last image
            if key == ord('a'):
                s = s - 2 if s >= 2 else 0
                l = l - 2 if l >= 2 else 0

            elif key == ord('n'):
                print('*** View Terminat & Relabel Discard ***\n')
                save = False

            # enter label mode
            elif key == ord('s'):
                print('------ Revise Labels Start ------')
                gb_img = seg_img.copy()
                gb_org = gb_img.copy()
                gb_no = len(gb_label) - 1
                # set mouse callback function
                seg_no = seg_imgs_path[s - 1].split('\\')[-1][:-4]
                print('... Segment No:%s ...' % seg_no)
                cv2.setMouseCallback('segment', relabel, [seg_no])
                while (1):
                    k = cv2.waitKey(0)
                    # withdraw the last label
                    if k == ord('z'):
                        if gb_no >= 0:
                            gb_label = gb_label.drop(index=gb_no)
                            gb_no -= 1
                            gb_newlabel -= 1
                        else:
                            gb_no = -1
                        cv2.imshow('segment', gb_org)
                        print(gb_label[-5:])
                    # quit label mode
                    elif k == ord('q'):
                        print('... Number of new labels: %d ...' % gb_newlabel)
                        print('------ Revise Labels End & Save ------\n')
                        break
                save = True
                cv2.destroyAllWindows()

        if save:
            gb_label.to_csv(relabel_path)

view_data()