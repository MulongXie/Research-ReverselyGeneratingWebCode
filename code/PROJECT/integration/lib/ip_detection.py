import cv2
import numpy as np

import ip_draw as draw
import ip_detection_utils as util
import ocr_classify_text as ocr


def get_corner(boundaries):
    """
    Get the top left and bottom right points of boundary
    :param boundaries: boundary: [top, bottom, left, right]
                        -> up, bottom: (column_index, min/max row border)
                        -> left, right: (row_index, min/max column border) detect range of each row
    :return: corners: [(top_left, bottom_right)]
                        -> top_left: (column_min, row_min)
                        -> bottom_right: (column_max, row_max)
    """
    corners = []
    for boundary in boundaries:
        top_left = (min(boundary[0][0][0], boundary[1][-1][0]), min(boundary[2][0][0], boundary[3][-1][0]))
        bottom_right = (max(boundary[0][0][0], boundary[1][-1][0]), max(boundary[2][0][0], boundary[3][-1][0]))
        corner = (top_left, bottom_right)
        corners.append(corner)
    return corners


def merge_corners(corners):
    """
    i. merge overlapped corners
    ii. remove nested corners
    :param corners: corners: [(top_left, bottom_right)]
                            -> top_left: (column_min, row_min)
                            -> bottom_right: (column_max, row_max)
    :return: new corners
    """
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


def uicomponent_or_block(org, corners, compo_max_height, compo_min_edge_ratio):
    """
    Select the potential ui components (button, input) from block objects
    :param org: Original image
    :param corners: corners: [(top_left, bottom_right)]
                            -> top_left: (column_min, row_min)
                            -> bottom_right: (column_max, row_max)
    :param compo_max_height: Over the threshold won't be counted
    :param compo_min_edge_ratio: Over the threshold won't be counted
    :return: corners of compos and blocks
    """
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


def img_or_block(org, binary, corners, max_thickness, max_block_cross_points):
    """
    Check if the objects are img components or just block
    :param org: Original image
    :param binary:  Binary image from pre-processing
    :param corners: [(top_left, bottom_right)]
                    -> top_left: (column_min, row_min)
                    -> bottom_right: (column_max, row_max)
    :param max_thickness: The max thickness of border of blocks
    :param max_block_cross_points: Ratio of point of interaction
    :return: corners of blocks and imgs
    """
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
                if np.sum(vacancy) == 4:
                    is_block = True
            except:
                pass
        if is_block:
            blocks.append(corner)
        else:
            imgs.append(corner)

    return blocks, imgs


def img_irregular(org, corners, must_img_height, must_img_width):
    """
    Select potential irregular shaped img elements by checking the height and width
    Check the edge ratio for img components to avoid text misrecognition
    :param org: Original image
    :param corners: [(top_left, bottom_right)]
                    -> top_left: (column_min, row_min)
                    -> bottom_right: (column_max, row_max)
    :param must_img_height: Larger is likely to be img
    :param must_img_width: Larger is likely to be img
    :return: corners of img
    """
    imgs = []
    for corner in corners:
        (up_left, bottom_right) = corner
        (y_min, x_min) = up_left
        (y_max, x_max) = bottom_right
        height = x_max - x_min
        width = y_max - y_min
        # assumption: large one must be img component no matter its edge ratio
        if height > must_img_height:
            imgs.append(corner)
    return imgs


def img_refine(org, corners, max_img_height_ratio, text_edge_ratio, text_height):
    """
    Remove too large imgs and likely text
    :param org: Original image
    :param corners: [(top_left, bottom_right)]
                    -> top_left: (column_min, row_min)
                    -> bottom_right: (column_max, row_max)
    :param max_img_height_ratio: height of img / total height of original image
    :param text_edge_ratio: width / height, if too large, then likely to be text
    :param text_height: common max height of text
    :return: corners of refined img
    """
    img_height, img_width = org.shape[:2]

    refined_imgs = []
    for corner in corners:
        (up_left, bottom_right) = corner
        (y_min, x_min) = up_left
        (y_max, x_max) = bottom_right
        height = x_max - x_min
        width = y_max - y_min

        # ignore too large ones
        if org.shape[0] > 1000 and height / img_height > max_img_height_ratio:
            continue
        # likely to be text, ignore
        elif height <= text_height and width / height > text_edge_ratio:
            continue
        refined_imgs.append(corner)

    return refined_imgs


# remove imgs that contain text
def rm_text(org, corners, must_img_height, must_img_width, ocr_padding, ocr_min_word_area, show=False):
    """
    Remove area that full of text
    :param org: original image
    :param corners: [(top_left, bottom_right)]
                    -> top_left: (column_min, row_min)
                    -> bottom_right: (column_max, row_max)
    :param must_img_height: Too large should be img
    :param must_img_width: Too large should be img
    :param ocr_padding: Padding for clipping
    :param ocr_min_word_area: If too text area ratio is too large
    :param show: Show or not
    :return: corners without text objects
    """
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


def rm_line(binary, lines):
    """
    Remove lines from binary map
    :param binary: Binary image
    :param lines: [line_h, line_v]
            -> line_h: horizontal {'head':(column_min, row), 'end':(column_max, row), 'thickness':int)
            -> line_v: vertical {'head':(column, row_min), 'end':(column, row_max), 'thickness':int}
    :return: New binary map with out lines
    """
    new_binary = binary.copy()
    line_h, line_v = lines
    for line in line_h:
        row = line['head'][1]
        new_binary[row: row + line['thickness'], line['head'][0]:line['end'][0]] = 0
    for line in line_v:
        column = line['head'][0]
        new_binary[line['head'][1]:line['end'][1], column: column + line['thickness']] = 0

    return new_binary


def line_detection(binary, min_line_length_h=200, min_line_length_v=80, max_thickness=3):
    """
    Detect lines
    :param binary: Binary image from pre-processing
    :param min_line_length_h: Min length for horizontal lines
    :param min_line_length_v: Min length for vertical lines
    :param max_thickness
    :return: lines: [line_h, line_v]
            -> line_h: horizontal {'head':(column_min, row), 'end':(column_max, row), 'thickness':int)
            -> line_v: vertical {'head':(column, row_min), 'end':(column, row_max), 'thickness':int}
    """
    def check(start_row, start_col, mode, line=None):
        if mode == 'h':
            for t in range(max_thickness + 1):
                if start_row + t >= binary.shape[0] or binary[start_row + t, start_col] == 0:
                    # if needed, update the thickness of this line
                    if line is not None:
                        line['thickness'] = max(line['thickness'], t)
                    return True
                mark_h[start_row + t, start_col] = 255
            return False
        elif mode == 'v':
            for t in range(max_thickness + 1):
                if start_col + t >= binary.shape[1] or binary[start_row, start_col + t] == 0:
                    # if needed, update the thickness of this line
                    if line is not None:
                        line['thickness'] = max(line['thickness'], t)
                    return True
                mark_v[start_row, start_col + t] = 255
            return False

    row, column = binary.shape[0], binary.shape[1]
    mark_h = np.zeros(binary.shape, dtype=np.uint8)
    mark_v = np.zeros(binary.shape, dtype=np.uint8)
    lines_h = []
    lines_v = []
    x, y = 0, 0
    while x < row - 1 or y < column - 1:
        # horizontal
        new_line = False
        head, end = None, None
        line = {}
        for j in range(column):
            # line start
            if not new_line and mark_h[x][j] == 0 and binary[x][j] > 0 and check(x, j, 'h'):
                head = j
                new_line = True
                line['head'] = (head, x)
                line['thickness'] = -1
            # line end
            elif new_line and (j == column - 1 or mark_h[x][j] > 0 or binary[x][j] == 0 or not check(x, j, 'h', line)):
                end = j
                new_line = False
                if end - head > min_line_length_h:
                    line['end'] = (end, x)
                    lines_h.append(line)
                line = {}

        # vertical
        new_line = False
        head, end = None, None
        line = {}
        for i in range(row):
            # line start
            if not new_line and mark_v[i][y] == 0 and binary[i][y] > 0 and check(i, y, 'v'):
                head = i
                new_line = True
                line['head'] = (y, head)
                line['thickness'] = 0
            # line end
            elif new_line and (i == row - 1 or mark_v[i][y] > 0 or binary[i][y] == 0 or not check(i, y, 'v', line)):
                end = i
                new_line = False
                if end - head > min_line_length_v:
                    line['end'] = (y, end)
                    lines_v.append(line)
                line = {}

        if x < row - 1:
            x += 1
        if y < column - 1:
            y += 1

    return lines_h, lines_v


# take the binary image as input
# calculate the connected regions -> get the bounding boundaries of them -> check if those regions are rectangles
# return all boundaries and boundaries of rectangles
def boundary_detection(binary, min_obj_area, min_obj_perimeter, min_line_thickness, min_rec_evenness, max_dent_ratio):
    """
    :param binary: Binary image from pre-processing
    :param min_obj_area: If not pass then ignore the small object
    :param min_obj_perimeter: If not pass then ignore the small object
    :param min_line_thickness: If not pass then ignore the slim object
    :param min_rec_evenness: If not pass then this object cannot be rectangular
    :param max_dent_ratio: If not pass then this object cannot be rectangular
    :return: boundary: [top, bottom, left, right]
                        -> up, bottom: (column_index, min/max row border)
                        -> left, right: (row_index, min/max column border) detect range of each row
    """
    mark = np.full(binary.shape, 0, dtype=np.uint8)
    boundary_all = []
    boundary_rec = []
    boundary_nonrec = []
    row, column = binary.shape[0], binary.shape[1]

    for i in range(row):
        for j in range(column):
            if binary[i, j] == 255 and mark[i, j] == 0:
                # get connected area
                area = util.bfs_connected_area(binary, i, j, mark)
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
