import cv2
import os
import pandas as pd

ix, iy = -1, -1
# global variables for visualisation
gb_img = None   # record the new label
gb_img_pre = None   # restore the new labels
gb_img_broad = None  # the drawing broad

gb_org = None   # copy of original image segment
gb_label = None  # label of this web page
gb_label_no = None  # index of the new line of label
gb_newlabelnum = 0


def add_label(label, ix, iy, x, y, segment_no):
    l = {'bx': ix, 'by': iy, 'bh': int(x - ix), 'bw': int(y - iy), 'segment_no': int(segment_no)}
    label = label.append(l, ignore_index=True)
    print('... Number of new labels: %d ...' % gb_newlabelnum)
    return label


def draw_label(label, img, segment_no):
    if len(label) == 0:
        print('----- No Label ------')
        return
    print(type(label['segment_no'][1]))
    label = label[label['segment_no'] == segment_no]
    print('------ Number of Labels Drawn:%d ------' % len(label))
    for i in range(len(label)):
        l = label.iloc[i]
        print(l)
        cv2.rectangle(img, (l['bx'], l['by']), (l['bx'] + l['bw'], l['by'] + l['bh']), (0, 0, 255), 2)
    cv2.imshow('segment', img)
    cv2.waitKey(0)


def relabel(event, x, y, flags, param):
    global ix, iy, gb_img, gb_img_pre, gb_img_broad,\
        gb_org, gb_label, gb_label_no, gb_newlabelnum
    seg_no = param[0]

    if event == cv2.EVENT_LBUTTONDOWN:
        # fetch the start points
        ix, iy = x, y
        gb_img_pre = gb_img.copy()
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        # draw the rectangle
        cv2.rectangle(gb_img, (ix, iy), (x, y), (0, 255, 0), -1)
        cv2.addWeighted(gb_org, 0.7, gb_img, 0.3, 0, gb_img_broad)
        cv2.imshow('segment', gb_img_broad)
        cv2.imshow('img', gb_img)
    elif event == cv2.EVENT_LBUTTONUP:
        # save the labeled area
        gb_label_no += 1
        gb_newlabelnum += 1
        gb_label = add_label(gb_label, ix, iy, x, y, seg_no)


def view_data(start_point, data_position='D:\datasets\dataset_webpage\data'):
    # *** step 1 *** Root Path
    # retrieve global variables for relabel
    global gb_img, gb_img_pre, gb_img_broad,\
        gb_org, gb_label, gb_label_no, gb_newlabelnum
    # set root path
    root = os.path.join(data_position, 'img_segment')
    img_root = os.path.join(root, 'img')
    label_root = os.path.join(root, 'label')
    relabel_root = os.path.join(root, 'label_refine')   # relabels path

    # *** step 2 *** Iterate Web Pages
    # iterate all web pages from the start point
    indices = sorted([int(l[:-4]) for l in os.listdir(label_root)])
    for index in indices[indices.index(start_point):]:
        # set paths
        img_path = os.path.join(img_root, str(index))
        img_path_segment = os.path.join(img_path, 'segment')
        img_path_labeled = os.path.join(img_path, 'labeled')
        label_path = os.path.join(label_root, str(index) + '.csv')
        relabel_path = os.path.join(relabel_root, str(index) + '.csv')

        print("\n*** Start Checking %s ***" % img_path)

        # retrieve paths of original images and labeled images
        seg_imgs_path = []
        labeled_imgs_path = []
        if os.path.exists(img_path_segment):
            seg_imgs_path = [p for p in os.listdir(img_path_segment)]
            seg_imgs_path.sort(key=lambda v: int(v[:-4]))  # sort by img index
            seg_imgs_path = [os.path.join(img_path_segment, p) for p in seg_imgs_path]
        if os.path.exists(img_path_labeled):
            labeled_imgs_path = [p for p in os.listdir(img_path_labeled)]
            labeled_imgs_path.sort(key=lambda v: int(v[:-4]))  # sort by img index
            labeled_imgs_path = [os.path.join(img_path_labeled, p) for p in labeled_imgs_path]
        # read existing label
        if os.path.exists(label_path):
            label = pd.read_csv(label_path, index_col=0)
            gb_label = label
            gb_newlabelnum = 0

        print(seg_imgs_path)
        print(labeled_imgs_path)

        # *** step 3 *** Iterate Segment Images
        # iterate all image segments for each web page
        s = 0
        l = 0
        seg_next = True
        lab_next = True
        save = False

        next = True
        sp = ''
        lp = ''
        while True:
            # read and show original image segments
            if s < len(seg_imgs_path) and os.path.exists(seg_imgs_path[s]):
                sp = seg_imgs_path[s]
                seg_img = cv2.imread(sp)
                # seg_img = cv2.resize(seg_img, (600, 300))
                gb_img = seg_img
                cv2.imshow('segment', gb_img)
            else:
                seg_next = False
            # read and show labeled image segments
            if l < len(labeled_imgs_path) and os.path.exists(labeled_imgs_path[l]):
                lp = labeled_imgs_path[l]
                lab_img = cv2.imread(lp)
                # lab_img = cv2.resize(lab_img, (600, 300))
                cv2.imshow('labeled', lab_img)
            else:
                lab_next = False
            if not seg_next and not lab_next:
                break

            if next:
                if sp is not '': print(sp)
                if lp is not '': print(lp)
                next = False

            # *** step 4 *** Web Page-Level Options
            # get the index of image segment and check image segment image on by one
            seg_no = int(seg_imgs_path[s].split('\\')[-1][:-4])
            key = cv2.waitKey(0)

            # back to the previous image
            if key == ord('a'):
                s = s - 1 if s >= 1 else 0
                l = l - 1 if l >= 1 else 0
            # remove all existing labels
            elif key == ord('c'):
                gb_label = gb_label.drop(index=gb_label.index.values)
                s = 0
                l = 0
                print('*** ! Remove All Label for This Page ! ***')
                continue
            # draw labels on the segment image
            elif key == ord('l'):
                draw_label(gb_label, gb_img, seg_no)
                continue
            # skip rest segment images and save the current relabel
            elif key == ord('e'):
                print('*** Relabel Saved ***\n')
                save = True
                break
            # skip rest segment images and discard the current relabel
            elif key == ord('q'):
                print('*** End Checking ***\n')
                save = False
                break
            # terminate the program
            elif key == ord('n'):
                print('\n*** Program Terminated ***')
                return

            # *** step 5 *** Segment-Level Options
            # enter label mode
            elif key == ord('s'):
                print('------ Revise Labels Start ------')
                gb_img_pre = gb_img.copy()
                gb_img_broad = gb_img.copy()
                gb_org = gb_img.copy()
                gb_label_no = len(gb_label) - 1
                # set mouse callback function
                print('... Segment No:%s ...' % seg_no)
                cv2.setMouseCallback('segment', relabel, [seg_no])
                while (1):
                    k = cv2.waitKey(0)
                    # withdraw the last label
                    if k == ord('z'):
                        if gb_label_no >= 0:
                            gb_label = gb_label.drop(index=gb_label_no)
                            gb_label_no -= 1
                            gb_newlabelnum -= 1
                        else:
                            gb_label_no = -1
                        gb_img = gb_img_pre.copy()
                        cv2.addWeighted(gb_org, 0.7, gb_img_pre, 0.3, 0, gb_img_broad)
                        cv2.imshow('segment', gb_img_broad)

                    # quit label mode
                    elif k == ord('d'):
                        print('------ Revise Labels End------')
                        break
                save = True

            else:
                s += 1
                l += 1
                next = True

        cv2.destroyAllWindows()
        if save:
            gb_label.to_csv(relabel_path)
            print('*** Relabels Saved to %s ***' % relabel_path)


view_data(16)