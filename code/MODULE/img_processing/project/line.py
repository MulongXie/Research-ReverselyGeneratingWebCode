import cv2
import numpy as np
import ip_preprocessing as pre


def draw_line(img, lines):
    broad = np.zeros(img.shape, dtype=np.uint8)
    for line in lines:
        cv2.line(img, line[0], line[1], (255, 0, 0))
    cv2.imshow('line', img)


def search_line(binary, min_line_length=100, max_thickness=3):
    row, column = binary.shape[0], binary.shape[1]

    lines = []
    for i in range(row - 1):
        head, end = -1, -1
        line = False
        for j in range(column - 1):
            if binary[i][j] > 0 and not line:
                head = j
                line = True
            elif binary[i][j] == 0 and line:
                end = j
                line = False
                if end - head > min_line_length:
                    # check if this line is too thick to be line
                    clear_top, clear_bottom = False, False
                    for t in range(max_thickness + 1):
                        if not clear_top and (i - t <= 0 or np.sum(binary[i - t, head:end])/255 < 5):
                            clear_top = True
                        if not clear_bottom and (i + t >= row - 1 or np.sum(binary[i + t, head:end])/255 < 5):
                            clear_bottom = True
                        if clear_top and clear_bottom:
                            lines.append(((head, i), (end, i)))
                            break
    print(lines)
    return lines


org, gray = pre.read_img('input/5.png', (0, 3000))  # cut out partial img
binary = pre.preprocess(gray, 1)
lines = search_line(binary)
draw_line(org, lines)

cv2.imshow('bin', binary)
cv2.waitKey(0)