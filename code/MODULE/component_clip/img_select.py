import shutil as shu

label_path = 'img_scr/label/'
labeled_img_path = 'img_scr/labeled_image/'
org_img_path = 'img_scr/screenshot/'

file = open('usable.txt')
for line in file.readlines():
    line = line[:-1]
    label = line + '.csv'
    labeled_img = line + '.png'
    org_img = line + '.png'

    shu.copy(label_path + label, 'img_select/usable_label/' + label)
    shu.copy(labeled_img_path + labeled_img, 'img_select/usable_labeled_img/' + labeled_img)
    shu.copy(org_img_path + org_img, 'img_select/usable_org/' + org_img)
