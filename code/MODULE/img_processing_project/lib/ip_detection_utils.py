import numpy as np
import cv2
from collections import Counter

import ip_draw as draw


# detect object(connected region)
def bfs_connected_area(img, x, y, mark):
    def neighbor(img, x, y, mark, stack):
        for i in range(x - 1, x + 2):
            if i < 0 or i >= img.shape[0]: continue
            for j in range(y - 1, y + 2):
                if j < 0 or j >= img.shape[1]: continue
                if img[i, j] == 255 and mark[i, j] == 0:
                    stack.append([i, j])
                    mark[i, j] = 255
                    
    stack = [[x, y]]    # points waiting for inspection
    area = [[x, y]]   # points of this area
    mark[x, y] = 255    # drawing broad

    while len(stack) > 0:
        point = stack.pop()
        area.append(point)
        neighbor(img, point[0], point[1], mark, stack)
    return area


# get the bounding boundary of an object(region)
# @boundary: [top, bottom, left, right]
# -> up, bottom: (column_index, min/max row border)
# -> left, right: (row_index, min/max column border) detect range of each row
def get_boundary(area):
    border_up, border_bottom, border_left, border_right = {}, {}, {}, {}
    for point in area:
        # point: (row_index, column_index)
        # up, bottom: (column_index, min/max row border) detect range of each column
        if point[1] not in border_up or border_up[point[1]] > point[0]:
            border_up[point[1]] = point[0]
        if point[1] not in border_bottom or border_bottom[point[1]] < point[0]:
            border_bottom[point[1]] = point[0]
        # left, right: (row_index, min/max column border) detect range of each row
        if point[0] not in border_left or border_left[point[0]] > point[1]:
            border_left[point[0]] = point[1]
        if point[0] not in border_right or border_right[point[0]] < point[1]:
            border_right[point[0]] = point[1]

    boundary = [border_up, border_bottom, border_left, border_right]
    # descending sort
    for i in range(len(boundary)):
        boundary[i] = [[k, boundary[i][k]] for k in boundary[i].keys()]
        boundary[i] = sorted(boundary[i], key=lambda x: x[0])
    return boundary


# check if an object is so slim
# @boundary: [border_up, border_bottom, border_left, border_right]
# -> up, bottom: (column_index, min/max row border)
# -> left, right: (row_index, min/max column border) detect range of each row
def clipping_by_line(boundary, boundary_rec, lines):
    boundary = boundary.copy()
    for orient in lines:
        # horizontal
        if orient == 'h':
            # column range of sub area
            r1, r2 = 0, 0
            for line in lines[orient]:
                if line[0] == 0:
                    r1 = line[1]
                    continue
                r2 = line[0]
                b_top = []
                b_bottom = []
                for i in range(len(boundary[0])):
                    if r2 > boundary[0][i][0] >= r1:
                        b_top.append(boundary[0][i])
                for i in range(len(boundary[1])):
                    if r2 > boundary[1][i][0] >= r1:
                        b_bottom.append(boundary[1][i])

                b_left = [x for x in boundary[2]]   # (row_index, min column border)
                for i in range(len(b_left)):
                    if b_left[i][1] < r1:
                        b_left[i][1] = r1
                b_right = [x for x in boundary[3]]  # (row_index, max column border)
                for i in range(len(b_right)):
                    if b_right[i][1] > r2:
                        b_right[i][1] = r2

                boundary_rec.append([b_top, b_bottom, b_left, b_right])
                r1 = line[1]


def is_line(boundary, min_line_thickness):
    # check if it is line by checking the length of edges
    if True in [len(boundary[i]) < min_line_thickness for i in range(len(boundary))]:
        return True
    return False


# i. detect if an object is rectangle by evenness of each border
# ii. add dent detection
# iii. add connected line detection
# @boundary: [border_up, border_bottom, border_left, border_right]
# -> up, bottom: (column_index, min/max row border)
# -> left, right: (row_index, min/max column border) detect range of each row
def is_rectangle(boundary, lines, min_rec_parameter, min_rec_evenness, min_line_thickness, min_line_length, max_dent_ratio, is_line_detect):
    opposite_side = [1, 0, 3, 2]  # opposite sides for each edges
    dent_direction = [-1, 1, -1, 1]

    flat = 0
    parameter = 0
    for n, border in enumerate(boundary):
        parameter += len(border)
        # dent detection
        dent = 0  # length of dent
        depth = 0  # depth of dent, vector
        if n <= 1:
            edge = max(len(boundary[2]), len(boundary[3]))  # get maximum length of adjacent edge
        else:
            edge = max(len(boundary[0]), len(boundary[1]))

        # line detection
        head, end = -1, -1  # start and end point of a line
        line = []  # line detected

        # -> up, bottom: (column_index, min/max row border)
        # -> left, right: (row_index, min/max column border) detect range of each row
        for i in range(len(border) - 1):
            # line detection
            if is_line_detect:
                if n == 0 or n == 2:
                    gap = abs(boundary[opposite_side[n]][i][1] - border[i][1])  # distance between points of opposite sides
                    if gap < min_line_thickness:
                        if head == -1:
                            head = border[i][0]  # new line start
                        else:
                            end = border[i][0]  # existing line extend
                    if head is not -1 and (gap >= min_line_thickness or i == len(border) - 2):
                        # line end
                        if end - head >= min_line_length:
                            line.append([head, end])
                        head, end = -1, -1

            # calculate gradient
            difference = border[i][1] - border[i + 1][1]
            if abs(difference) == 0:
                flat += 1
            # too abnormal to be a regular shape
            elif abs(difference) / edge > 0.6:
                return False

            # dent detection
            depth += difference
            # if dent and too deep, then counted as dent
            if dent_direction[n] * depth > 0 and abs(depth) / edge > 0.2:
                dent += 1

        if dent / len(border) > max_dent_ratio:
            return False

        if is_line_detect:
            if n == 0 and len(line) > 0:
                lines['h'] = line   # horizontally
            elif n == 2 and len(line) > 0:
                lines['v'] = line   # vertically

    # ignore text and irregular shape
    if parameter < min_rec_parameter or (flat / parameter) < min_rec_evenness:
        return False
    return True


def contain(corner_a, corner_b):
    (up_left_a, bottom_right_a) = corner_a
    (y_min_a, x_min_a) = up_left_a
    (y_max_a, x_max_a) = bottom_right_a
    (up_left_b, bottom_right_b) = corner_b
    (y_min_b, x_min_b) = up_left_b
    (y_max_b, x_max_b) = bottom_right_b

    # if a is in b
    if y_min_a > y_min_b and x_min_a > x_min_b and y_max_a < y_max_b and x_max_a < x_max_b:
        return -1
    # if b is in a
    elif y_min_a < y_min_b and x_min_a < x_min_b and y_max_a > y_max_b and x_max_a > x_max_b:
        return 1
    return 0

