import pandas as pd
import cv2
import numpy as np


def draw_block(lines, upper, lower, is_drawn=False):
    r, g, b = 255, 255, 255
    for i, line in enumerate(lines):
        t_l = line[0]
        b_r = (line[1][0], lower[i])
        cv2.rectangle(img, t_l, b_r, (b, g, r), -1)
        cv2.imwrite('output/low/' + str(i) + '.png', img)
        if b > 0:
            b -= 25
        else:
            r -= 25


def read_lines(lines):
    lines_converted = []
    for i in range(len(lines)):
        line = lines.iloc[i]
        head = tuple([int(h) for h in line['head'][1:-1].split(', ')])
        end = tuple([int(h) for h in line['end'][1:-1].split(', ')])
        lines_converted.append((head, end))
    return lines_converted


# clean those lines so close to others that can be treated as the part of other line
def merge_close_lines(lines):
    # merge list members that are closer than the threshold
    def tight_set(list, thresh):
        index_row = [i[0] for i in list]
        index_row = sorted(index_row)
        list_tight = [list[0]]
        anchor = 0
        mark = anchor
        for i in range(1, len(index_row)):
            if index_row[i] - index_row[mark] <= thresh:
                mark = i
                continue
            else:
                list_tight.append(list[i])
                anchor = i
                mark = anchor
        return list_tight

    # check if there is any existing approximate range of line (column of head to column of end)
    def approximate_range(range, ranges, thresh=5):
        for r in ranges:
            if abs(range[0] - r[0]) + abs(range[1] - r[1]) < thresh:
                return r
        return -1

    # group lines in {'[range of column]': (row index, line index)}
    lines_formatted = {}
    for i, line in enumerate(lines):
        pos = (line[0][0], line[1][0])
        key = approximate_range(pos, lines_formatted.keys())
        # no approximate range existing
        if key == -1:
            if pos not in lines_formatted:
                lines_formatted[pos] = [(line[0][1], i)]
            else:
                lines_formatted[pos].append((line[0][1], i))
        else:
            lines_formatted[key].append((line[0][1], i))

    new_lines = []
    for r in lines_formatted:
        for l in [lines[t[1]] for t in tight_set(lines_formatted[r], 3)]:
            new_lines.append(l)

    return new_lines


# lines: [(head, end)] -> [((col, row), (col, row))]
# axi = 0 divide horizontally
# axi = 1 divide vertically
def divide_blocks(lines, height, axi):
    lines = merge_close_lines(lines)

    upper = np.zeros(len(lines), dtype=int)  # y of upper bound for each line
    lower = np.full(len(lines), height)  # y of lower bound for each line

    for i in range(len(lines)):
        for j in range(len(lines)):
            if i == j:
                continue
            head_i, end_i = lines[i][0], lines[i][1]
            head_j, end_j = lines[j][0], lines[j][1]
            if not ((head_i[0] <= head_j[0] and end_i[0] > end_j[0]) or (head_i[0] < head_j[0] and end_i[0] >= end_j[0])):
                if head_i[1] > head_j[1] > upper[i]:
                    upper[i] = head_j[1]
                if head_i[1] < head_j[1] < lower[i]:
                    lower[i] = head_j[1]

    pack_block(lines, upper, lower)

    return upper, lower


img = cv2.imread('input/4.png')
line_h = pd.read_csv('output/line_h.csv', index_col=0)
line_v = pd.read_csv('output/line_v.csv', index_col=0)

line_h = read_lines(line_h)
line_v = read_lines(line_v)

upper, lower = divide_blocks(line_h, img.shape[0], 0)

# draw_line(broad, line_h, (255, 0, 0))
# draw_line(broad, line_v, (0, 0, 255))
# cv2.imwrite('output/lines.png', broad)
