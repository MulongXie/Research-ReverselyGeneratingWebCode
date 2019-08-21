import cv2
import numpy as np
import ip_preprocessing as pre


def draw_line(img, lines, color, show=True):
    for line in lines:
        cv2.line(img, line[0], line[1], color)
        cv2.imshow('img', img)
        cv2.waitKey(0)


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


def search_line(binary, min_line_length_h=200, min_line_length_v=80, max_thickness=3, max_cross_point=0.1):
    row, column = binary.shape[0], binary.shape[1]

    lines_h = []
    lines_v = []
    x, y = 0, 0
    while x < row - 1 or y < column - 1:
        # horizontal
        line = False
        head, end = -1, -1
        for j in range(column):
            # line start
            if binary[x][j] > 0 and not line:
                head = j
                line = True
            # line end
            elif binary[x][j] == 0 and line:
                end = j
                line = False
                if end - head > min_line_length_h:
                    # check if this line is too thick to be line
                    clear_top, clear_bottom = False, False
                    for t in range(max_thickness + 1):
                        if not clear_top and (x - t <= 0 or (np.sum(binary[x - t, head:end])/255) / (end-head) < max_cross_point):
                            clear_top = True
                        if not clear_bottom and (x + t >= row - 1 or (np.sum(binary[x + t, head:end])/255) / (end-head) < max_cross_point):
                            clear_bottom = True
                        if clear_top and clear_bottom:
                            lines_h.append(((head, x), (end, x)))
                            break
        # vertical
        line = False
        head, end = -1, -1
        for i in range(row):
            if binary[i][y] > 0 and not line:
                head = i
                line = True
            elif (binary[i][y] == 0 or i >= row - 1) and line:
                end = i
                line = False
                if end - head > min_line_length_v:
                    # check if this line is too thick to be line
                    clear_left, clear_right = False, False
                    for t in range(max_thickness + 1):
                        if not clear_left and (y - t <= 0 or (np.sum(binary[head:end, y - t])/255) / (end-head) < max_cross_point):
                            clear_left = True
                        if not clear_right and (y + t >= column - 1 or (np.sum(binary[head:end, y + t])/255) / (end-head) < max_cross_point):
                            clear_right = True
                        if clear_left and clear_right:
                            lines_v.append(((y, head), (y, end)))
                            break
        if x < row - 1:
            x += 1
        if y < column - 1:
            y += 1

    return lines_h, lines_v


org, gray = pre.read_img('input/18.png', (2000, 2600))  # cut out partial img
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
