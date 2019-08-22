from collections import Counter


# check if an object is so slim
# @boundary: [border_up, border_bottom, border_left, border_right]
# -> up, bottom: (column_index, min/max row border)
# -> left, right: (row_index, min/max column border) detect range of each row
def is_line(boundary, min_line_thickness):
    # up and bottom
    difference = [abs(boundary[0][i][1] - boundary[1][i][1]) for i in range(len(boundary[1]))]
    most, number = Counter(difference).most_common(1)[0]
    # too slim
    if most < min_line_thickness:
        return True
    # left and right
    difference = [abs(boundary[2][i][1] - boundary[3][i][1]) for i in range(len(boundary[2]))]
    most, number = Counter(difference).most_common(1)[0]
    # too slim
    if most < min_line_thickness:
        return True
    return False