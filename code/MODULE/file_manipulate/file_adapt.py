import pandas as pd
import os


def move_file():
    root_label = 'D:\datasets\dataset_webpage\data\img_segment\label_refine'
    des_label = 'D:\datasets\dataset_webpage\data\img_relabelled\label'

    scr = 'D:\datasets\dataset_webpage\data\img_segment\img'
    des = 'D:\datasets\dataset_webpage\data\img_relabelled\img'
    for f in os.listdir(root_label):
        index = f[:-4]
        os.renames(os.path.join(scr, index), os.path.join(des, index))
        os.renames(os.path.join(root_label, f), os.path.join(des_label, f))


def box_convert(label):
    x_min = label['bx']
    y_min = label['by']
    x_max = x_min + label['bw']
    y_max = y_min + label['bh']
    return " " + str(x_min) + "," + str(y_min) + "," + str(x_max) + "," + str(y_max) + ",0"


def label_convert(label_root, img_root, output_path):
    label_news = ""
    indices = os.listdir(os.path.join(label_root))
    indices = sorted([int(i[:-4]) for i in indices])
    for index in indices:
        label_path = os.path.join(label_root, str(index) + '.csv')
        img_path = os.path.join(img_root, str(index) + '\segment')

        print(label_path)

        label = pd.read_csv(label_path)
        if len(label) == 0:
            print("%s is empty" % label_path)
            continue
        label_new = {}
        for i in range(len(label)):
            l = label.iloc[i]
            seg_no = str(int(l['segment_no']))
            if seg_no not in label_new:
                label_new[seg_no] = os.path.join(img_path, seg_no + ".png")
            label_new[seg_no] += box_convert(l)

        if len(label_new) > 0:
            label_news += "\n".join(label_new.values())
            label_news += '\n'

        f = open(output_path, 'w')
        f.write(label_news)
    return label_news


# remove path pointing into images without <img> label
def label_refine(label_path, refine_label_path):
    org_label = open(label_path)

    refine = ""
    is_refine = False
    for l in org_label.readlines():
        img_path = l.split(' ')[0]
        label_path = img_path.replace('\segment', '\labeled')

        try:
            open(label_path)
            refine += l
        except:
            print("No <img> label for %s" % img_path)
            is_refine = True

    if is_refine:
        refine_label = open(refine_label_path, 'w')
        refine_label.write(refine)


# convert to format for colab
def label_colab(label_path, label_colab_path):
    labels = open(label_path)
    label_colab = open(label_colab_path, 'w')
    for label in labels.readlines():
        label = label.replace('D:\datasets\dataset_webpage\\', './')
        label = label.replace('\\', '/')
        label_colab.write(label)


data_position = 'D:\datasets\dataset_webpage\data'
root = os.path.join(data_position, 'img_relabelled')
img_root = os.path.join(root, 'img')
label_root = os.path.join(root, 'label')

label_convert(label_root, img_root, os.path.join(root, 'label.txt'))
# label_refine(os.path.join(root, 'label.txt'), os.path.join(root, 'label_refine.txt'))
label_colab(os.path.join(root, 'label.txt'), os.path.join(root, 'label_colab.txt'))