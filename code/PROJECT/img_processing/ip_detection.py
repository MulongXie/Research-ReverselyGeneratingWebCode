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
    # descending sort
    for i in range(len(boundary)):
        boundary[i] = sorted(boundary[i].items(), key=lambda x: x[0])

    return boundary


def get_corner(boundaries):
    corners = []
    for boundary in boundaries:
        up_left = (boundary[0][0][0], boundary[2][0][0])
        bottom_right = (boundary[1][-1][0], boundary[3][-1][0])
        corners.append((up_left, bottom_right))
    return corners


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


def is_wireframe(binary, corners, max_thickness):

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


# get the more accurate bounding box of rectangles
def rec_refine(binary, corners, max_thickness):
    refined_corners = []
    # remove inner rectangles
    corners = rm_inner_rec(corners)

    for corner in corners:
        (up_left, bottom_right) = corner
        (y_min, x_min) = up_left
        (y_max, x_max) = bottom_right

        width = y_max - y_min - 2 * max_thickness
        height = x_max - x_min - 2 * max_thickness

        # line: count_divide_column > 0.9
        # background: count_divide_column < 0.1
        # scan horizontally
        for x in range(x_min + max_thickness, x_max - max_thickness):
            count_divide_column = np.sum(binary[x, y_min+max_thickness: y_max-max_thickness])/255/width
            count_divide_column_pre = np.sum(binary[x-max_thickness, y_min+max_thickness: y_max-max_thickness])/255/width
            # left inner border: current column is line (all one) + previous column is background (all zero)
            if count_divide_column > 0.9 and count_divide_column_pre == 0:
                if x_max - x > max_thickness and x - x_min > max_thickness:
                    x_min = x
            # right inner border: current column is background (all zero) + previous column is
            elif count_divide_column == 0 and count_divide_column_pre > 0.9:
                if x - x_min > max_thickness and x_max - x > max_thickness:
                    x_max = x - max_thickness

        # scan vertically
        for y in range(y_min + max_thickness, y_max - max_thickness):
            count_divide_column = np.sum(binary[x_min+max_thickness: x_max-max_thickness, y])/255/height
            count_divide_column_pre = np.sum(binary[x_min+max_thickness: x_max-max_thickness, y-max_thickness])/255/height
            # left inner border: current column is line (all one) + previous column is background (all zero)
            if count_divide_column > 0.9 and count_divide_column_pre == 0:
                if y_max - y > max_thickness and y - y_min > max_thickness:
                    y_min = y
            # right inner border: current column is background (all zero) + previous column is
            elif count_divide_column == 0 and count_divide_column_pre > 0.9:
                if y - y_min > max_thickness and y_max - y > max_thickness:
                    y_max = y - max_thickness

        refined_corners.append(((y_min, x_min), (y_max, x_max)))
    return refined_corners


# detect if it is rectangle by evenness of each border
# @boundary: [border_up, border_bottom, border_left, border_right]
def is_rectangle(boundary, min_rec_parameter, min_rec_evenness, max_rec_edge_ratio, min_line_thickness):
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
    edge_ratio = len(boundary[0]) / len(boundary[2]) if len(boundary[0]) >= len(boundary[2]) else len(boundary[2]) / len(boundary[0])

    # ignore text and irregular shape
    if parameter < min_rec_parameter or edge_ratio > max_rec_edge_ratio or (evenness / parameter) < min_rec_evenness:
        return False
    return True


# take the binary image as input
def boundary_detection(bin, min_obj_area, min_rec_parameter, min_rec_evenness, max_rec_edge_ratio, min_line_thickness):
    mark = np.full(bin.shape, 0, dtype=np.uint8)
    boundary_all = []
    boundary_rec = []
    row, column = bin.shape[0], bin.shape[1]

    for i in range(row):
        for j in range(column):
            if bin[i, j] == 255 and mark[i, j] == 0:
                area = bfs_connected_area(bin, i, j, mark)
                # ignore all small area
                if len(area) > min_obj_area:
                    boundary = get_boundary(area)
                    boundary_all.append(boundary)
                    if is_rectangle(boundary, min_rec_parameter, min_rec_evenness, max_rec_edge_ratio, min_line_thickness):
                        boundary_rec.append(boundary)

    return boundary_all, boundary_rec
