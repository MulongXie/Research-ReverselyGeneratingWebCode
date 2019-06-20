import cv2
import numpy as np


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


def draw_boundary(boundary, broad):
    # draw
    for b in boundary:
        b_sp = b.split('_')
        if b_sp[0] == 'row':
            broad[int(b_sp[2]), boundary[b]] = 255
        elif b_sp[0] == 'col':
            broad[boundary[b], int(b_sp[2])] = 255


def get_boundary(area):
    up, bottom, left, right = (None, None, None, None)
    boundary = {}
    for point in area:
        # range of each row by checking y
        b_left = 'row_min_' + str(point[0])
        b_right = 'row_max_' + str(point[0])
        # range of each column by checking x
        b_up = 'col_min_' + str(point[1])
        b_bottom = 'col_max_' + str(point[1])
        if b_left not in boundary or boundary[b_left] > point[1]:
            boundary[b_left] = point[1]
        if b_right not in boundary or boundary[b_right] < point[1]:
            boundary[b_right] = point[1]
        if b_up not in boundary or boundary[b_up] > point[0]:
            boundary[b_up] = point[0]
        if b_bottom not in boundary or boundary[b_bottom] < point[0]:
            boundary[b_bottom] = point[0]

        if up is None or up > point[0]:
            up = point[0]
        if bottom is None or bottom < point[0]:
            bottom = point[0]
        if left is None or left > point[1]:
            left = point[1]
        if right is None or right < point[1]:
            right = point[1]

    extremum = (up, bottom, left, right)

    return boundary, extremum


def is_rectangle(boundary, extremum, thresh=0.8):
    (up, bottom, left, right) = extremum

    fit_up, fit_bottom, fit_left, fit_right = (0, 0, 0, 0)  # count the fit points
    len_up, len_bottom, len_left, len_right = (0, 0, 0, 0)  # count the length of boundary

    for b in boundary:
        b_sp = b.split('_')
        if b_sp[0] == 'row':
            if b_sp[1] == 'min':
                len_left += 1
                if (abs(boundary[b] - left)) == 0:
                    fit_left += 1
            if b_sp[1] == 'max':
                len_right += 1
                if abs(boundary[b] - right) == 0:
                    fit_right += 1
        if b_sp[0] == 'col':
            if b_sp[1] == 'min':
                len_up += 1
                if abs(boundary[b] - up) == 0:
                    fit_up += 1
            if b_sp[1] == 'max':
                len_bottom += 1
                if abs(boundary[b] - bottom) == 0:
                    fit_bottom += 1

    print("up: %d zeros in %d length" % (fit_up, len_up))
    print("bottom: %d zeros in %d length" % (fit_bottom, len_bottom))
    print("left: %d zeros in %d length" % (fit_left, len_left))
    print("right: %d zeros in %d length" % (fit_right, len_right))
    print('\n')

    if (fit_up / len_up) < thresh or (fit_bottom / len_bottom) < thresh\
        or (fit_left / len_left) < thresh or (fit_right / len_right) < thresh:
        return False

    return True

def scan(img):
    mark = np.full(img.shape, 0, dtype=np.uint8)
    bound = mark.copy()
    row, column = img.shape[0], img.shape[1]

    for i in range(row):
        for j in range(column):
            if img[i, j] == 255 and mark[i, j] == 0:
                area = bfs_connected_area(img, i, j, mark)
                boundary, extremum = get_boundary(area)

                if is_rectangle(boundary, extremum):
                    draw_boundary(boundary, bound)

                    cv2.imshow('org', img)
                    cv2.imshow('mark', mark)
                    cv2.imshow('boundary', bound)
                    cv2.waitKey(0)


# img = np.zeros((600, 600, 3), dtype=np.uint8)
# img[30:50, 30:50, :] = 255
# img[90:138, 50:76, :] = 255
# img[100:103, 66:70] = 0
# img[220: 230, :, :] = 255

img = cv2.imread('c_close.png')
img = img[600: 1200, :]
#
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
r, bin = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
bin_copy = bin.copy()

scan(bin_copy)
