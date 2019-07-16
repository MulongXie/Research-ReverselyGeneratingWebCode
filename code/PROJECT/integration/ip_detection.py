import cv2
import numpy as np

import ip_draw as draw
import ip_detection_utils as util


def get_corner(boundaries):
    corners = []
    for boundary in boundaries:
        up_left = (boundary[0][0][0], boundary[2][0][0])
        bottom_right = (boundary[1][-1][0], boundary[3][-1][0])
        corners.append((up_left, bottom_right))
    return corners


# check if the objects are img components or just frame
def frame_or_img(binary, corners, max_thickness):
    frames = []
    imgs = []
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
            frames.append(corner)
        else:
            imgs.append(corner)
    return frames, imgs


# get the more accurate bounding box of img components
def img_refine(binary, corners, max_thickness):
    refined_corners = []
    # remove inner rectangles
    # corners = util.rm_inner_rec(corners)

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


# check the edge ratio for img components
def img_refine2(rec_corners, max_img_edge_ratio):
    refined_corners = []
    for corner in rec_corners:
        (up_left, bottom_right) = corner
        (y_min, x_min) = up_left
        (y_max, x_max) = bottom_right
        width = y_max - y_min
        height = x_max - x_min
        edge_ratio = width/height if width > height else height/width
        if edge_ratio < max_img_edge_ratio:
            refined_corners.append(corner)
    return refined_corners


# take the binary image as input
# calculate the connected regions -> get the bounding boundaries of them -> check if those regions are rectangles
# return all boundaries and boundaries of rectangles
def boundary_detection(bin, min_obj_area, min_rec_parameter, min_rec_evenness, min_line_thickness):
    mark = np.full(bin.shape, 0, dtype=np.uint8)
    boundary_all = []
    boundary_rec = []
    row, column = bin.shape[0], bin.shape[1]

    for i in range(row):
        for j in range(column):
            if bin[i, j] == 255 and mark[i, j] == 0:
                area = util.bfs_connected_area(bin, i, j, mark)
                # ignore all small area
                if len(area) > min_obj_area:
                    boundary = util.get_boundary(area)
                    boundary_all.append(boundary)
                    if util.is_rectangle(boundary, min_rec_parameter, min_rec_evenness, min_line_thickness):
                        boundary_rec.append(boundary)
    return boundary_all, boundary_rec
