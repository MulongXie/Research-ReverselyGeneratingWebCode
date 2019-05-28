import cv2
import shutil
import pandas as pd


def sort_index(c):
    print(c[:-4])
    return int(c[:-4])


s = ['1.csv', '3.csv', '10.csv', '5.csv']
s.sort(key=sort_index)

print(s)