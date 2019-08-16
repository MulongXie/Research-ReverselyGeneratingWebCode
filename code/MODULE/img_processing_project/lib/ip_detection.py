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
def block_or_img(org, binary, corners, max_thickness, max_block_cross_points, text_edge_ratio, text_height):
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
            # likely to be text, ignore
            if not (height <= text_height and width/height > text_edge_ratio):
                imgs.append(corner)
    return blocks, imgs


# check the edge ratio for img components to avoid text misrecognition
def irregular_img(org, corners, must_img_height, must_img_width, text_edge_ratio, text_height):
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
        else:
            # likely to be text, ignore
            if not(height <= text_height and width/height > text_edge_ratio):
                imgs.append(corner)
    return imgs


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
            # check if this area is text
            clip = org[x_min - ocr_padding: x_max + ocr_padding, y_min - ocr_padding: y_max + ocr_padding]
            if not ocr.is_text(clip, ocr_min_word_area, show=show):
                new_corners.append(corner)
    return new_corners


# remove imgs that are in others
def rm_inner_rec(corners):
    inner = np.full((len(corners), 1), False)
    for i in range(len(corners)):
        for j in range(i+1, len(corners)):
            # if [i] is in [j]
            if util.contain(corners[i], corners[j]) == -1:
                inner[i] = True
            # if [j] is in [i]
            elif util.contain(corners[i], corners[j]) == 1:
                inner[j] = True
    refined_corners = []
    for i in range(len(inner)):
        if not inner[i]:
            refined_corners.append(corners[i])
    return refined_corners


# take the binary image as input
# calculate the connected regions -> get the bounding boundaries of them -> check if those regions are rectangles
# return all boundaries and boundaries of rectangles
def boundary_detection(bin, min_obj_area, min_obj_perimeter, min_line_thickness, min_line_length, min_rec_evenness, max_dent_ratio):
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

                if util.is_rectangle(boundary, min_rec_evenness, max_dent_ratio):
                    boundary_rec.append(boundary)
                else:
                    boundary_nonrec.append(boundary)

    return boundary_all, boundary_rec, boundary_nonrec
