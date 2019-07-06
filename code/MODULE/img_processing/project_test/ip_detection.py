import cv2
import numpy as np
from collections import Counter

import ip_draw as draw


def neighbor(img, x, y, mark, stack):
    for i in range(x - 1, x + 2):
        if i < 0 or i >= img.shape[0]: continue
        for j in range(y - 1, y + 2):
            if j < 0 or j >= img.shape[1]: continue
            if img[i, j] == 255 and mark[i, j] == 0:
                stack.append([i, j])
                mark[i, j] = 255


def bfs_connected_area(img, x, y, mark):
    stack = [[x, y]]    # points waiting for inspection
    area = [[x, y]]   # points of this area
    mark[x, y] = 255    # drawing broad

    while len(stack) > 0:
        point = stack.pop()
        area.append(point)
        neighbor(img, point[0], point[1], mark, stack)
    return area


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
    for i in range(len(boundary)):
        boundary[i] = sorted(boundary[i].items(), key=lambda x: x[0])

    return boundary


def get_corner(boundaries):
    corners = []
    for bounary in boundaries:
        up_left = (bounary[0][0][0], bounary[2][0][0])
        bottom_right = (bounary[1][-1][0], bounary[3][-1][0])
        corners.append((up_left, bottom_right))
    return corners


def is_line(boundary, min_gap=10):
    # up and bottom
    difference = [abs(boundary[0][i][1] - boundary[1][i][1]) for i in range(len(boundary[1]))]
    most, number = Counter(difference).most_common(1)[0]
    # too slim
    if most < min_gap:
        return True
    # left and right
    difference = [abs(boundary[2][i][1] - boundary[3][i][1]) for i in range(len(boundary[2]))]
    most, number = Counter(difference).most_common(1)[0]
    # too slim
    if most < min_gap:
        return True

    return False


def is_wireframe(binary, corners, max_thickness=6):

    wireframes = []
    non_wireframe = []
    for corner in corners:
        (up_left, bottom_right) = corner
        (y_min, x_min) = up_left
        (y_max, x_max) = bottom_right

        is_wire = False
        vacancy = [0, 0, 0, 0]
        for i in range(1, max_thickness):
            # up down
            if vacancy[0] == 0 and (np.sum(binary[x_min + i, y_min + i: y_max - i])/255)/(y_max-y_min-2*i) <= 0.1:
                vacancy[0] = 1
            # bottom-up
            if vacancy[1] == 0 and (np.sum(binary[x_max - i, y_min + i: y_max - i])/255)/(y_max-y_min-2*i) <= 0.1:
                vacancy[1] = 1
            # left to right
            if vacancy[2] == 0 and (np.sum(binary[x_min + i: x_max - i, y_min + i])/255)/(x_max-x_min-2*i) <= 0.1:
                vacancy[2] = 1
            # right to left
            if vacancy[3] == 0 and (np.sum(binary[x_min + i: x_max - i, y_max - i])/255)/(x_max-x_min-2*i) <= 0.1:
                vacancy[3] = 1

            if np.sum(vacancy) == 4:
                is_wire = True

        if is_wire:
            wireframes.append(corner)
        else:
            non_wireframe.append(corner)

    return wireframes, non_wireframe


def rec_compress(binary, corners, max_thickness=6):

    compressed_corners = []
    for corner in corners:
        (up_left, bottom_right) = corner
        (y_min, x_min) = up_left
        (y_max, x_max) = bottom_right

        width = y_max - y_min - 2 * max_thickness
        height = x_max - x_min - 2 * max_thickness

        # scan vertically
        count_divide_column_pre = np.sum(binary[x_min + max_thickness: x_max - max_thickness, y_min + max_thickness])/255/height
        for y in range(y_min + max_thickness + 1, y_max - max_thickness):
            count_divide_column = np.sum(binary[x_min + max_thickness: x_max - max_thickness, y])/255/height

            # left inner border: current column is line (all one) + previous column is background (all zero)
            if count_divide_column > 0.9 and count_divide_column_pre == 0:
                y_min = y
            # right inner border: current column is background (all zero) + previous column is line (all one)
            if count_divide_column == 0 and count_divide_column_pre > 0.9:
                y_max = y

            count_divide_column_pre = count_divide_column

        compressed_corners.append(((y_min, x_min), (y_max, x_max)))

    return compressed_corners


# detect if it is rectangle by evenness of each border
def is_rectangle(boundary, min_parameter=100, min_evenness=0.8):
    if is_line(boundary):
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
    if parameter < min_parameter or (evenness / parameter) < min_evenness:
        return False

    return True


# take the binary image as input
def boundary_detection(bin, min_area=200):
    mark = np.full(bin.shape, 0, dtype=np.uint8)
    boundary_all = []
    boundary_rec = []
    row, column = bin.shape[0], bin.shape[1]

    for i in range(row):
        for j in range(column):
            if bin[i, j] == 255 and mark[i, j] == 0:
                area = bfs_connected_area(bin, i, j, mark)
                # ignore all small area
                if len(area) > min_area:
                    boundary = get_boundary(area)
                    boundary_all.append(boundary)
                    if is_rectangle(boundary):
                        boundary_rec.append(boundary)

    return boundary_all, boundary_rec
