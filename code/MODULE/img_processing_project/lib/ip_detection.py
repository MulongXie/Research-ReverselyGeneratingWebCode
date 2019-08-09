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


# check if the objects are img components or just block
# return corners ((y_min, x_min),(y_max, x_max))
def block_or_img(binary, corners, max_thickness, max_block_cross_points):
    blocks = []
    imgs = []
    for corner in corners:
        (up_left, bottom_right) = corner
        (y_min, x_min) = up_left
        (y_max, x_max) = bottom_right

        is_block = False
        vacancy = [0, 0, 0, 0]
        for i in range(1, max_thickness):
            # up down
            if vacancy[0] == 0 and (np.sum(binary[x_min + i, y_min + i: y_max - i])/255)/(y_max-y_min-2*i) <= max_block_cross_points:
                vacancy[0] = 1
            # bottom-up
            if vacancy[1] == 0 and (np.sum(binary[x_max - i, y_min + i: y_max - i])/255)/(y_max-y_min-2*i) <= max_block_cross_points:
                vacancy[1] = 1
            # left to right
            if vacancy[2] == 0 and (np.sum(binary[x_min + i: x_max - i, y_min + i])/255)/(x_max-x_min-2*i) <= max_block_cross_points:
                vacancy[2] = 1
            # right to left
            if vacancy[3] == 0 and (np.sum(binary[x_min + i: x_max - i, y_max - i])/255)/(x_max-x_min-2*i) <= max_block_cross_points:
                vacancy[3] = 1
            if np.sum(vacancy) == 4:
                is_block = True

        if is_block:
            blocks.append(corner)
        else:
            imgs.append(corner)
    return blocks, imgs


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


# check the edge ratio for img components to avoid text misrecognition
def img_refine2(rec_corners, max_img_edge_ratio, must_img_height, must_img_width):
    refined_corners = []
    for corner in rec_corners:
        (up_left, bottom_right) = corner
        (y_min, x_min) = up_left
        (y_max, x_max) = bottom_right
        width = y_max - y_min
        height = x_max - x_min
        # assumption: large one must be img component no matter its edge ratio
        if height > must_img_height or width > must_img_width:
            refined_corners.append(corner)
        else:
            edge_ratio = width/height if width > height else height/width
            if edge_ratio < max_img_edge_ratio:
                refined_corners.append(corner)
    return refined_corners


# take the binary image as input
# calculate the connected regions -> get the bounding boundaries of them -> check if those regions are rectangles
# return all boundaries and boundaries of rectangles
def boundary_detection(bin, min_obj_area, min_rec_parameter, min_rec_evenness, min_line_thickness, min_line_length, max_dent_ratio):
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
                    lines = {}  # connected lines inner boundary
                    boundary = util.get_boundary(area)
                    boundary_all.append(boundary)
                    if util.is_rectangle(boundary, lines, min_rec_parameter, min_rec_evenness, min_line_thickness, min_line_length, max_dent_ratio):
                        boundary_rec.append(boundary)

                        # means this object can be divided into two sub objects connected by line
                        if len(lines) > 0:
                            print(lines)
                            p = util.clipping_by_line(boundary, lines, bin.shape)
                    # draw.draw_test(boundary_all, bin.shape)
    return boundary_rec, boundary_all


def text_detection(gradient, boundary_all):
    corners_text = []
    corners = get_corner(boundary_all)
    for corner in corners:
        (up_left, bottom_right) = corner
        (y_min, x_min) = up_left
        (y_max, x_max) = bottom_right
        width = y_max - y_min
        height = x_max - x_min

        edge_ratio = width/height
        if edge_ratio > 1.5 and height < 20:
            corners_text.append(corner)

        print(height)
        print("%.3f\n" % (width/height))

    return corners_text
