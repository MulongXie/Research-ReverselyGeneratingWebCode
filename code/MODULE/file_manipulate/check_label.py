import os


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


def count_box(label_path):
    label = open(label_path)
    for l in label.readlines():
        box = l.split(' ')
        print(len(box))
        print(box)


label_refine('label_refine.txt', '')
# count_box('D:\datasets\dataset_webpage\data\img_segment\\label_refine.txt')