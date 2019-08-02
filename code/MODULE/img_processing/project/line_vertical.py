import cv2
import numpy as np
import ip_preprocessing as pre


def draw_line(img, lines, color):
    for line in lines:
        cv2.line(img, line[0], line[1], color)


def search_line(binary, min_line_length_h=200, min_line_length_v=300, max_thickness=3, max_cross_points=30):
    row, column = binary.shape[0], binary.shape[1]

    lines_h = []
    lines_v = []
    x, y = 0, 0
    while x < row - 1 or y < column - 1:
        # horizontal
        line = False
        head, end = -1, -1
        for j in range(column):
            if binary[x][j] > 0 and not line:
                head = j
                line = True
            elif binary[x][j] == 0 and line:
                end = j
                line = False
                if end - head > min_line_length_h:
                    # check if this line is too thick to be line
                    clear_top, clear_bottom = False, False
                    for t in range(max_thickness + 1):
                        if not clear_top and (x - t <= 0 or np.sum(binary[x - t, head:end])/255 < max_cross_points):
                            clear_top = True
                        if not clear_bottom and (x + t >= row - 1 or np.sum(binary[x + t, head:end])/255 < max_cross_points):
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
                        if not clear_left and (y - t <= 0 or np.sum(binary[head:end, y - t])/255 < max_cross_points):
                            clear_left = True
                        if not clear_right and (y + t >= column - 1 or np.sum(binary[head:end, y + t])/255 < max_cross_points):
                            clear_right = True
                        if clear_left and clear_right:
                            lines_v.append(((y, head), (y, end)))
                            break
        if x < row - 1:
            x += 1
        if y < column - 1:
            y += 1

    return lines_h, lines_v


org, gray = pre.read_img('input/4.png', (0, 3000))  # cut out partial img
binary = pre.preprocess(gray, 1)
lines_h, lines_v = search_line(binary)
draw_line(org, lines_h, (0, 255, 0))
draw_line(org, lines_v, (0, 0, 255))

cv2.imwrite('output/labeled.png', org)
cv2.imwrite('output/grad.png', binary)
