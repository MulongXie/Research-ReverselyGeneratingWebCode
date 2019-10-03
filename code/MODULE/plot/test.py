from os.path import join as pjoin
import os
import json
import glob

label_root = 'E:\Mulong\Result\web\\ui_label'
paths = glob.glob(pjoin(label_root, '*.json'))

heights = []
widths = []
ratios = []

for path in paths:
    compo_f = open(path, 'r')
    compos = json.load(compo_f)
    for compo in compos['compos']:
        if compo['class'] == 'div':
            heights.append(int(compo['height']))
            widths.append(int(compo['width']))
            ratios.append(int(compo['width']) / int(compo['height']))
