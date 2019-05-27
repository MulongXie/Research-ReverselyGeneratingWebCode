import cv2
import os

data_position = 'D:\datasets\dataset_webpage\data'
root = os.path.join(data_position, 'img_segment')
img_root = os.path.join(root, 'img')
label_root = os.path.join(root, 'label')

labels = os.listdir(label_root)

c_seg = 0
c_labeled = 0
# iterate each web page
for label in labels:
    index = label[:-4]
    img_path = os.path.join(img_root, index)
    img_path_segment = os.path.join(img_path, 'segment')
    img_path_labeled = os.path.join(img_path, 'labeled')

    seg_imgs = []
    labeled_imgs = []
    if os.path.exists(img_path_segment):
        c_seg += 1
        seg_imgs = [os.path.join(img_path_segment, p) for p in os.listdir(img_path_segment)]
    if os.path.exists(img_path_labeled):
        c_labeled += 1
        labeled_imgs = [os.path.join(img_path_labeled, p) for p in os.listdir(img_path_labeled)]

    s = 0
    l = 0
    while s != 9999 and l != 9999:
        if s < len(seg_imgs) and os.path.exists(seg_imgs[s]):
            print(seg_imgs[s])
            seg = cv2.imread(seg_imgs[s])
            cv2.imshow('segment', seg)
            s += 1
        else:
            s = 9999
        if l < len(labeled_imgs) and os.path.exists(labeled_imgs[l]):
            print(labeled_imgs[l], '\n')
            lab = cv2.imread(labeled_imgs[l])
            cv2.imshow('labeled', lab)
            l += 1
        else:
            l = 9999
        cv2.waitKey(0)

print(c_seg)
print(c_labeled)