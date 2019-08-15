import cv2
import numpy as np

import ip_draw as draw
import ip_detection_utils as util
import ocr_classify_text as ocr


def get_corner(boundaries):
    corners = []
    for boundary in boundaries:
        up_left = (boundary[0][0][0], boundary[2][0][0])
        bottom_right = (boundary[1][-1][0], boundary[3][-1][0])
        corners.append((up_left, bottom_right))
    return corners


# check if the objects are img components or just block
# return corners ((y_min, x_min),(y_max, x_max))
def block_or_img(binary, corners, max_thickness, max_block_cross_points, max_img_edge_ratio):
    blocks = []
    imgs = []
    for corner in corners:
        (up_left, bottom_right) = corner
        (y_min, x_min) = up_left
        (y_max, x_max) = bottom_right
        width = y_max - y_min
        height = x_max - x_min

        is_block = False
        vacancy = [0, 0, 0, 0]
        for i in range(1, max_thickness):
            try:
                # up down
                if vacancy[0] == 0 and (y_max - y_min - 2 * i) is not 0 and (
                        np.sum(binary[x_min + i, y_min + i: y_max - i]) / 255) / (y_max - y_min - 2 * i) <= max_block_cross_points:
                    vacancy[0] = 1
                # bottom-up
                if vacancy[1] == 0 and (y_max - y_min - 2 * i) is not 0 and (
                        np.sum(binary[x_max - i, y_min + i: y_max - i]) / 255) / (y_max - y_min - 2 * i) <= max_block_cross_points:
                    vacancy[1] = 1
                # left to right
                if vacancy[2] == 0 and (x_max - x_min - 2 * i) is not 0 and (
                        np.sum(binary[x_min + i: x_max - i, y_min + i]) / 255) / (x_max - x_min - 2 * i) <= max_block_cross_points:
                    vacancy[2] = 1
                # right to left
                if vacancy[3] == 0 and (x_max - x_min - 2 * i) is not 0 and (
                        np.sum(binary[x_min + i: x_max - i, y_max - i]) / 255) / (x_max - x_min - 2 * i) <= max_block_cross_points:
                    vacancy[3] = 1
                if np.sum(vacancy) == 4:
                    is_block = True
            except:
                pass
        if is_block:
            blocks.append(corner)
        else:
            edge_ratio = width / height if width > height else height / width
            if edge_ratio <= max_img_edge_ratio:
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
def irregular_img(org, corners, max_img_edge_ratio, must_img_height, must_img_width, min_perimeter, ocr_padding, ocr_min_word_area):
    img_corners = []
    for corner in corners:
        (up_left, bottom_right) = corner
        (y_min, x_min) = up_left
        (y_max, x_max) = bottom_right
        height = x_max - x_min
        width = y_max - y_min
        perimeter = width * 2 + height * 2

        # assumption: large one must be img component no matter its edge ratio
        if height > must_img_height and width > must_img_width:
            img_corners.append(corner)
        else:
            if perimeter > min_perimeter and width/height < max_img_edge_ratio:
                # check if this area is text
                clip = org[x_min-ocr_padding: x_max+ocr_padding, y_min-ocr_padding: y_max+ocr_padding]
                if not ocr.is_text(clip, ocr_min_word_area, show=False):
                    img_corners.append(corner)

    return img_corners


# take the binary image as input
# calculate the connected regions -> get the bounding boundaries of them -> check if those regions are rectangles
# return all boundaries and boundaries of rectangles
def boundary_detection(bin, min_obj_area, min_rec_parameter, min_rec_evenness, min_line_thickness, min_line_length, max_dent_ratio, detect_line=False):
    mark = np.full(bin.shape, 0, dtype=np.uint8)
    boundary_all = []
    boundary_rec = []
    boundary_nonrec = []
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
                    # check if it is line by checking the length of edges
                    if util.is_line(boundary, min_line_thickness):
                        continue
                    if util.is_rectangle(boundary, lines, min_rec_parameter, min_rec_evenness, min_line_thickness, min_line_length, max_dent_ratio, detect_line):
                        # means this object can be divided into two sub objects connected by line
                        if detect_line and len(lines) > 0:
                            util.clipping_by_line(boundary, boundary_rec, lines)
                        else:
                            boundary_rec.append(boundary)
                    else:
                        boundary_nonrec.append(boundary)

    return boundary_all, boundary_rec, boundary_nonrec

