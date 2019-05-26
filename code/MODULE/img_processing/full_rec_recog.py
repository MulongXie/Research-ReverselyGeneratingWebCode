import cv2
import numpy as np


def count_column(img, mask, a, b, height):
    count = 0
    for i in range(a, a+height):
        if img[i, b] == 255 and mask[i, b] == 0:
            count += 1
            mask[i, b] = 255

    return count


def count_row(img, mask, a, b, width):
    count = 0
    for j in range(b, b+width):
        if img[a, j] == 255 and mask[a, j] == 0:
            count += 1
            mask[a, j] = 255
    return count


def check_rec(img, mask, x, y):
    check_row = True
    check_column = True
    width = 1
    height = 1
    i = 1
    j = 1
    while check_row or check_column:
        if check_column:
            width += 1
            cc = count_column(img, mask, x, y + j, height)  # scan column (x, y+j),(x+1, y+j),(x+2, y+j)...(x+height, y+j)
            # if this column has no enough points, it is out of the object's border
            if cc / height < 0.1:
                check_column = False
                width -= 1
        if check_row:
            height += 1
            cr = count_row(img, mask, x + i, y, width)      # scan row (x+i, y),(x+i,y+1),(x+i,y+2)...(x+i, y+width)
            # if this row has no enough points, it is out of the object's border
            if cr / width < 0.3:
                check_row = False
                height -= 1

        print("cc:%d cr:%d" % (cc, cr))
        print('width:%d height:%d ' % (width, height))

        i += 1
        j += 1

    return width, height


def locate_point(img):
    mask = np.zeros(img.shape, dtype=np.uint8)
    row = img.shape[0]
    column = img.shape[1]

    rectangles = []
    for i in range(row):
        for j in range(column):
            rectangle = {}
            if img[i, j] == 255 and mask[i, j] == 0:
                rectangle['x'] = i
                rectangle['y'] = j
                rectangle['width'], rectangle['height'] = check_rec(img, mask, i, j)
                rectangles.append(rectangle)

    cv2.imshow('mask', mask)
    return rectangles


img = np.zeros((600, 600), dtype=np.uint8)
img[30:70, 200:320] = 255
img[90:138, 50:76] = 255

recs = locate_point(img)
print(recs)

cv2.imshow('img', img)
cv2.waitKey(0)