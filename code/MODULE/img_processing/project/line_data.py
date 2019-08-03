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


def tight_set(list, thresh):
    list = sorted(list)
    list_tight = [list[0]]
    anchor = 0
    for i in range(1, len(list) - 1):
        if list[i] - list[anchor] < thresh:
            continue
        else:
            list_tight.append(i)
            anchor = i
    return list_tight


# axi = 0 divide horizontally
# axi = 1 divide vertically
def divide_blocks(lines, axi):
    # group lines in {'[range]': row/column index}
    hier = {}
    for line in lines:
        pos = '[' + str(line[0][0]) + '-' + str(line[1][0]) + ']'
        if pos not in hier:
            hier[pos] = [line[0][1]]
        else:
            hier[pos].append(line[0][1])

    blocks = []
    for h in hier:
        print(h, hier[h])


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