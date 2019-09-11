def nms(corner_a, corner_b):
    corners_new = []

    corner_a = np.array(corner_a)
    corner_b = np.array(corner_b)
    for a in corner_a:
        # get the intersected area
        col_min_s = np.maximum(a[0], corner_b[:, 0])
        row_min_s = np.maximum(a[1], corner_b[:, 1])
        col_max_s = np.maximum(a[2], corner_b[:, 2])
        row_max_s = np.maximum(a[3], corner_b[:, 3])

        w = np.maximum(0, col_max_s - col_min_s + 1)
        h = np.maximum(0, row_max_s - row_min_s + 1)
        inter = w * h
        print(inter)

    return corners_new