import numpy as np

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
