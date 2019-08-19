import cv2
import numpy as np


def draw_bounding_box_class(corners, org, compo_class, color, line=3, show=False):
    """
    :param corners: ((column_min, row_min),(column_max, row_max))
    :param org: original image
    :param color: line color
    :param line: line thickness
    :param compo_class: classes matching the corners of components
    :param show: show or not
    :return: labeled image
    """
    if compo_class is None:
        compo_class = ['compo' for i in range(len(corners))]
    broad = org.copy()
    for i in range(len(corners)):
        broad = cv2.rectangle(broad, corners[i][0], corners[i][1], color[compo_class[i]], line)
        broad = cv2.putText(broad, compo_class[i], (corners[i][0][0]+5, corners[i][0][1]+20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color[compo_class[i]], 2)
    if show:
        cv2.imshow('a', broad)
        cv2.waitKey(0)
    return broad


def draw_bounding_box(corners, org, color=(0, 255, 0), line=3, show=False):
    """
    :param corners: ((column_min, row_min),(column_max, row_max))
    :param org: original image
    :param color: line color
    :param line: line thickness
    :param show: show or not
    :return: labeled image
    """
    broad = org.copy()
    for i in range(len(corners)):
        broad = cv2.rectangle(broad, corners[i][0], corners[i][1], color, line)
    if show:
        cv2.imshow('a', broad)
        cv2.waitKey(0)
    return broad


def draw_boundary(boundaries, shape, show=False):
    broad = np.zeros(shape[:2], dtype=np.uint8)  # binary broad

    for boundary in boundaries:
        # up and bottom: (column_index, min/max row border)
        for point in boundary[0] + boundary[1]:
            broad[point[1], point[0]] = 255
        # left, right: (row_index, min/max column border)
        for point in boundary[2] + boundary[3]:
            broad[point[0], point[1]] = 255

    if show:
        cv2.imshow('rec', broad)
        cv2.waitKey(0)
    return broad
