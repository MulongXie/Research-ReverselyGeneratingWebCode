import numpy as np
import cv2
from collections import Counter


def neighbor(img, x, y, mark, stack):
    for i in range(x - 1, x + 2):
        if i < 0 or i >= img.shape[0]: continue
        for j in range(y - 1, y + 2):
            if j < 0 or j >= img.shape[1]: continue
            if img[i, j] == 255 and mark[i, j] == 0:
                stack.append([i, j])
                mark[i, j] = 255


# detect object(connected region)
# return area(points(x, y))
def bfs_connected_area(img, x, y, mark):
    stack = [[x, y]]    # points waiting for inspection
    area = [[x, y]]   # points of this area
    mark[x, y] = 255    # drawing broad

    while len(stack) > 0:
        point = stack.pop()
        area.append(point)
        neighbor(img, point[0], point[1], mark, stack)
    return area


# get the bounding boundary of an object(region)
# return boundary((column_index, min row border), (column_index, max row border),
# (row_index, min column border), (row_index, max column border))
def get_boundary(area):
    border_up, border_bottom, border_left, border_right = ({}, {}, {}, {})
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
        boundary[i] = sorted(boundary[i].items(), key=lambda x: x[0])
    return boundary


# check if an object is so slim
def is_line(boundary, min_line_thickness):
    # up and bottom
    difference = [abs(boundary[0][i][1] - boundary[1][i][1]) for i in range(len(boundary[1]))]
    most, number = Counter(difference).most_common(1)[0]
    # too slim
    if most < min_line_thickness:
        return True
    # left and right
    difference = [abs(boundary[2][i][1] - boundary[3][i][1]) for i in range(len(boundary[2]))]
    most, number = Counter(difference).most_common(1)[0]
    # too slim
    if most < min_line_thickness:
        return True
    return False


# detect if an object is rectangle by evenness of each border
# @boundary: [border_up, border_bottom, border_left, border_right]
def is_rectangle(boundary, min_rec_parameter, min_rec_evenness, min_line_thickness):
    if is_line(boundary, min_line_thickness):
        return False
    # up, bottom: (column_index, min/max row border)
    # left, right: (row_index, min/max column border)
    evenness = 0
    parameter = 0
    for border in boundary:
        parameter += len(border)
        # calculate the evenness of each border
        for i in range(len(border) - 1):
            if border[i][1] - border[i + 1][1] == 0:
                evenness += 1
    # ignore text and irregular shape
    if parameter < min_rec_parameter or (evenness / parameter) < min_rec_evenness:
        return False
    return True


# remove imgs that are in others
def rm_inner_rec(corners):
    inner = np.full((len(corners), 1), False)
    for i in range(len(corners)):
        (up_left_a, bottom_right_a) = corners[i]
        (y_min_a, x_min_a) = up_left_a
        (y_max_a, x_max_a) = bottom_right_a

        for j in range(i+1, len(corners)):
            (up_left_b, bottom_right_b) = corners[j]
            (y_min_b, x_min_b) = up_left_b
            (y_max_b, x_max_b) = bottom_right_b

            # if rec[i] is in rec[j]
            if y_min_a > y_min_b and x_min_a > x_min_b and y_max_a < y_max_b and x_max_a < x_max_b:
                inner[i] = True
            # if rec[i] is in rec[j]
            elif y_min_a < y_min_b and x_min_a < x_min_b and y_max_a > y_max_b and x_max_a > x_max_b:
                inner[j] = True
    refined_corners = []
    for i in range(len(inner)):
        if not inner[i]:
            refined_corners.append(corners[i])
    return refined_corners
