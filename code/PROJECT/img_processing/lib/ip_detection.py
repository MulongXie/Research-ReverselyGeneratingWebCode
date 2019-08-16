import cv2
import numpy as np

import ip_draw as draw
import ip_detection_utils as util
import ocr_classify_text as ocr


# @corners: [(top_left, bottom_right)]
# -> top_left: (column_min, row_min)
# -> bottom_right: (column_max, row_max)
def get_corner(boundaries):
    corners = []
    for boundary in boundaries:
        top_left = (min(boundary[0][0][0], boundary[1][-1][0]), min(boundary[2][0][0], boundary[3][-1][0]))
        bottom_right = (max(boundary[0][0][0], boundary[1][-1][0]), max(boundary[2][0][0], boundary[3][-1][0]))
        corner = (top_left, bottom_right)
        corners.append(corner)
    return corners


def uicomponent_or_block(corners, compo_max_height, compo_min_edge_ratio):
    compos = []
    blocks = []
    for corner in corners:
        (up_left, bottom_right) = corner
        (y_min, x_min) = up_left
        (y_max, x_max) = bottom_right
        height = x_max - x_min
        width = y_max - y_min

        if height <= compo_max_height and width/height >= compo_min_edge_ratio:
            compos.append(corner)
        else:
            blocks.append(corner)
    return blocks, compos


# check if the objects are img components or just block
# return corners ((y_min, x_min),(y_max, x_max))
def img_or_block(org, binary, corners, max_thickness, max_block_cross_points):
    blocks = []
    imgs = []
    for corner in corners:
        (up_left, bottom_right) = corner
        (y_min, x_min) = up_left
        (y_max, x_max) = bottom_right

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
                if np.sum(vacancy) >= 3:
                    is_block = True
            except:
                pass
        if is_block:
            blocks.append(corner)
        else:
            imgs.append(corner)
    return blocks, imgs


# check the edge ratio for img components to avoid text misrecognition
def img_irregular(org, corners, must_img_height, must_img_width):
    imgs = []
    for corner in corners:
        (up_left, bottom_right) = corner
        (y_min, x_min) = up_left
        (y_max, x_max) = bottom_right
        height = x_max - x_min
        width = y_max - y_min
        # assumption: large one must be img component no matter its edge ratio
        if height > must_img_height and width > must_img_width:
            imgs.append(corner)
    return imgs


def img_refine(org_shape, corners, max_img_height_ratio, text_edge_ratio, text_height):
    img_height, img_width = org_shape[:2]

    refined_imgs = []
    for corner in corners:
        (up_left, bottom_right) = corner
        (y_min, x_min) = up_left
        (y_max, x_max) = bottom_right
        height = x_max - x_min
        width = y_max - y_min

        # ignore too large ones
        if height / img_height > max_img_height_ratio:
            continue
        # likely to be text, ignore
        elif height <= text_height and width / height > text_edge_ratio:
            continue
        refined_imgs.append(corner)
    return refined_imgs


# remove imgs that contain text
def rm_text(org, corners, must_img_height, must_img_width, ocr_padding, ocr_min_word_area, show=False):
    new_corners = []
    for corner in corners:
        (up_left, bottom_right) = corner
        (y_min, x_min) = up_left
        (y_max, x_max) = bottom_right
        height = x_max - x_min
        width = y_max - y_min
        # highly likely to be block or img if too large
        if height > must_img_height and width > must_img_width:
            new_corners.append(corner)
        else:
            x_min = x_min - ocr_padding if x_min - ocr_padding >= 0 else 0
            x_max = x_max + ocr_padding if x_max + ocr_padding < org.shape[0] else org.shape[0]
            y_min = y_min - ocr_padding if y_min - ocr_padding >= 0 else 0
            y_max = y_max + ocr_padding if y_max + ocr_padding < org.shape[1] else org.shape[1]
            # check if this area is text
            clip = org[x_min: x_max, y_min: y_max]
            if not ocr.is_text(clip, ocr_min_word_area, show=show):
                new_corners.append(corner)
    return new_corners


# i. merge overlapped corners
# ii. remove nested corners
def merge_corners(corners):

    def merge_overlapped(corner_a, corner_b):
        (up_left_a, bottom_right_a) = corner_a
        (y_min_a, x_min_a) = up_left_a
        (y_max_a, x_max_a) = bottom_right_a
        (up_left_b, bottom_right_b) = corner_b
        (y_min_b, x_min_b) = up_left_b
        (y_max_b, x_max_b) = bottom_right_b

        y_min = min(y_min_a, y_min_b)
        y_max = max(y_max_a, y_max_b)
        x_min = min(x_min_a, x_min_b)
        x_max = max(x_max_a, x_max_b)
        return ((y_min, x_min), (y_max, x_max))

    new_corners = []
    for corner in corners:
        is_intersected = False
        for i in range(len(new_corners)):
            r = util.relation(corner, new_corners[i])
            # if corner is in new_corners[i], ignore corner
            if r == -1:
                is_intersected = True
                break
            # if new_corners[i] is in corner, replace corners[i] with corner
            elif r == 1:
                is_intersected = True
                new_corners[i] = corner
            # if [i] and [j] are overlapped
            if r == 2:
                is_intersected = True
                new_corners[i] = merge_overlapped(corner, new_corners[i])

        if not is_intersected:
            new_corners.append(corner)
    return new_corners


# take the binary image as input
# calculate the connected regions -> get the bounding boundaries of them -> check if those regions are rectangles
# return all boundaries and boundaries of rectangles
# @boundary: [top, bottom, left, right]
# -> up, bottom: (column_index, min/max row border)
# -> left, right: (row_index, min/max column border) detect range of each row
def boundary_detection(bin, min_obj_area, min_obj_perimeter, min_line_thickness, min_rec_evenness, max_dent_ratio):
    mark = np.full(bin.shape, 0, dtype=np.uint8)
    boundary_all = []
    boundary_rec = []
    boundary_nonrec = []
    row, column = bin.shape[0], bin.shape[1]

    for i in range(row):
        for j in range(column):
            if bin[i, j] == 255 and mark[i, j] == 0:
                # get connected area
                area = util.bfs_connected_area(bin, i, j, mark)
                # ignore small area
                if len(area) < min_obj_area:
                    continue

                # calculate the boundary of the connected area
                boundary = util.get_boundary(area)
                # ignore small area
                perimeter = np.sum([len(b) for b in boundary])
                if perimeter < min_obj_perimeter:
                    continue

                boundary_all.append(boundary)
                # check if it is line by checking the length of edges
                if util.is_line(boundary, min_line_thickness):
                    continue

                # rectangle check
                if util.is_rectangle(boundary, min_rec_evenness, max_dent_ratio):
                    boundary_rec.append(boundary)
                else:
                    boundary_nonrec.append(boundary)
    return boundary_all, boundary_rec, boundary_nonrec
