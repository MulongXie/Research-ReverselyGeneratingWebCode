import pandas as pd
import cv2
import numpy as np


def draw_line(img, lines, color):
    for line in lines:
        cv2.line(img, line[0], line[1], color)


def read_lines(lines):
    lines_converted = []
    for i in range(len(lines)):
        line = lines.iloc[i]
        head = tuple([int(h) for h in line['head'][1:-1].split(', ')])
        end = tuple([int(h) for h in line['end'][1:-1].split(', ')])
        lines_converted.append((head, end))
    return lines_converted


# axi = 0 divide horizontally
# axi = 1 divide vertically
def divide_blocks(lines, axi):

    top = np.zeros(len(lines))
    for line in lines:




img = cv2.imread('input/4.png')
line_h = pd.read_csv('output/line_h.csv', index_col=0)
line_v = pd.read_csv('output/line_v.csv', index_col=0)

line_h = read_lines(line_h)
line_v = read_lines(line_v)

divide_blocks(line_h, 0)

# broad = np.zeros(img.shape, dtype=np.uint8)
# draw_line(broad, line_h, (255, 0, 0))
# draw_line(broad, line_v, (0, 0, 255))
# cv2.imwrite('output/lines.png', broad)
