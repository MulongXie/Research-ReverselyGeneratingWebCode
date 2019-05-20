import cv2
import pandas as pd
import numpy as np

img = cv2.imread('0.png')
label = pd.read_csv('0.csv', index_col=0)
print(label.columns.values)
label_new = pd.DataFrame(columns=label.columns.values)

index = 0
for i in range(len(label)):
    compo = label.iloc[i]
    clip = img[compo['by']:compo['by'] + compo['bh'], compo['bx']:compo['bx'] + compo['bw'], :]
    avg_pix = clip.sum() / (clip.shape[0] * clip.shape[1] * clip.shape[2])
    if avg_pix < 245:
        label_new.loc[index] = compo
        index += 1
print(label_new)