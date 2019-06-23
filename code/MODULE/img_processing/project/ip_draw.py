import cv2
import numpy as np


def draw_bounding_box(corners, org, color=(0, 255, 0), line=3):
    broad = org.copy()
    for corner in corners:
        broad = cv2.rectangle(broad, corner[0], corner[1], color, line)

    return broad


def draw_boundary(boundaries, shape):
    broad = np.zeros(shape[:2], dtype=np.uint8)  # binary broad

    for boundary in boundaries:
        # up and bottom: (column_index, min/max row border)
        for point in boundary[0] + boundary[1]:
            broad[point[1], point[0]] = 255
        # left, right: (row_index, min/max column border)
        for point in boundary[2] + boundary[3]:
            broad[point[0], point[1]] = 255

    return broad
