import cv2


class BLOCK:
    # (column, row)
    def __init__(self, id, top_left, bottom_right):
        self.id = id
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.width = bottom_right[0] - top_left[0]
        self.height = bottom_right[1] - top_left[1]
        self.area = self.width * self.height
        self.parent = None
        self.child = None

    def draw_block(self, broad, color, thickness=-1, is_write=False, output=None):
        cv2.rectangle(broad, self.top_left, self.bottom_right, tuple(color), thickness)
        if is_write:
            cv2.imwrite(output, broad)

    # -1: contained by other block
    # 1: contains other block
    # 0: otherwise
    def hierarchy(self, block):
        tl_a, br_a = self.top_left, self.bottom_right
        tl_b, br_b = block.top_left, block.bottom_right
        # a contains b
        if tl_a[0] <= tl_b[0] and tl_a[1] <= tl_b[1] and \
                br_a[0] >= br_b[0] and br_a[1] >= br_b[1]:
            return 1
        # b contains a
        if tl_a[0] >= tl_b[0] and tl_a[1] >= tl_b[1] and \
                br_a[0] <= br_b[0] and br_a[1] <= br_b[1]:
            return -1
        else:
            return 0

    # only judged by the area of block
    def __le__(self, block):
        return True if self.area < block.area else False

    def __gt__(self, block):
        return True if self.area > block.area else False
