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

    merged_corners = []
    inner = np.full((len(corners), 1), False)
    for i in range(len(corners)):
        for j in range(i+1, len(corners)):
            r = util.relation(corners[i], corners[j])
            # if [i] is in [j]
            if r == -1:
                inner[i] = True
            # if [j] is in [i]
            elif r == 1:
                inner[j] = True
            # if [i] and [j] are overlapped
            elif r == 2:
                merged_corners.append(merge_overlapped(corners[i], corners[j]))

    for i in range(len(inner)):
        if not inner[i]:
            merged_corners.append(corners[i])
    return merged_corners