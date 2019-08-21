import cv2
import numpy as np
import ip_preprocessing as pre


def draw_line(img, lines, color, show=True):
    for line in lines:
        cv2.line(img, line[0], line[1], color)
        # cv2.imshow('img', img)
        # cv2.waitKey(0)


def rm_line(binary, lines):
    """
    Remove lines from binary map
    :param binary: Binary image
    :param lines: [line_h, line_v]
            -> line_h: horizontal ((column_min, row), (column_max, row))
            -> line_v: vertical ((column, row_min), (column, row_max))
    :return: New binary map
    """
    new_binary = binary.copy()
    line_h, line_v = lines
    for line in line_h:
        row = line[0][1]
        new_binary[row, line[0][0]:line[1][0]] = 0
    for line in line_v:
        column = line[0][0]
        new_binary[line[0][1]:line[1][1], column] = 0

    return new_binary


def search_line(binary, min_line_length_h=200, min_line_length_v=80, max_thickness=3):

    def check(start_row, start_col, mode):
        if mode == 'h':
            for t in range(max_thickness + 1):
                if start_row + t >= binary.shape[0] or binary[start_row + t, start_col] == 0:
                    return True
                mark_h[start_row + t, start_col] = 255
            return False
        elif mode == 'v':
            for t in range(max_thickness + 1):
                if start_col + t >= binary.shape[1] or binary[start_row, start_col + t] == 0:
                    return True
                mark_v[start_row, start_col + t] = 255
            return False

    row, column = binary.shape[0], binary.shape[1]

    mark_h = np.zeros(binary.shape, dtype=np.uint8)
    mark_v = np.zeros(binary.shape, dtype=np.uint8)
    lines_h = []
    lines_v = []
    x, y = 0, 0
    while x < row - 1 or y < column - 1:
        # horizontal
        new_line = False
        head, end = None, None
        for j in range(column):
            # line start
            if not new_line and mark_h[x][j] == 0 and binary[x][j] > 0 and check(x, j, 'h'):
                head = j
                new_line = True
            # line end
            elif new_line and (j == column - 1 or mark_h[x][j] > 0 or binary[x][j] == 0 or not check(x, j, 'h')):
                end = j
                new_line = False
                if end - head > min_line_length_h:
                    lines_h.append(((head, x), (end, x)))

        # vertical
        new_line = False
        head, end = None, None
        for i in range(row):
            # line start
            if not new_line and mark_v[i][y] == 0 and binary[i][y] > 0 and check(i, y, 'v'):
                head = i
                new_line = True
            # line end
            elif new_line and (i == row - 1 or mark_v[i][y] > 0 or binary[i][y] == 0 or not check(i, y, 'v')):
                end = i
                new_line = False
                if end - head > min_line_length_v:
                    lines_v.append(((y, head), (y, end)))
        if x < row - 1:
            x += 1
        if y < column - 1:
            y += 1

    print(len(lines_h), len(lines_v))
    return lines_h, lines_v


org, gray = pre.read_img('input/6.png', (2000, 2600))  # cut out partial img
binary = pre.preprocess(gray, 1)
lines_h, lines_v = search_line(binary)
draw_line(org, lines_h, (0, 255, 0))
draw_line(org, lines_v, (0, 0, 255))

broad = np.zeros(org.shape, dtype=np.uint8)
draw_line(broad, lines_h, (0, 255, 0))
draw_line(broad, lines_v, (0, 0, 255))

new_bin = rm_line(binary, [lines_h, lines_v])

cv2.imwrite('output/labeled.png', org)
cv2.imwrite('output/lines.png', broad)
cv2.imwrite('output/grad.png', binary)
cv2.imwrite('output/rm_line.png', new_bin)
