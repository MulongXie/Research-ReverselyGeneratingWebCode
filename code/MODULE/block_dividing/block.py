import cv2


class BLOCK:
    # (column, row)
    def __init__(self, id, top_left, bottom_right, parent=None, child=None, layer=None):
        self.id = id
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.parent = parent
        self.child = child
        self.layer = layer

        self.center = (int((bottom_right[0] + top_left[0])/2), int((bottom_right[1] + top_left[1])/2))
        self.width = bottom_right[0] - top_left[0]
        self.height = bottom_right[1] - top_left[1]
        self.area = self.width * self.height

        # calculate according to its parent block
        self.margin = []

    # only judged by the area of block
    def __le__(self, block):
        return True if self.area < block.area else False

    def __gt__(self, block):
        return True if self.area > block.area else False

    def draw_block(self, broad, color, thickness=-1, is_write=False, output=None):
        cv2.rectangle(broad, self.top_left, self.bottom_right, tuple(color), thickness)
        cv2.putText(broad, str(self.layer), self.center, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0,0), 2, cv2.LINE_AA)
        print(self.margin)
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

    def get_relative_position(self):
        # top, right, bottom
        parent = self.parent
        self.margin = [abs(self.top_left[1] - parent.top_left[1]),
                       abs(self.bottom_right[0] - parent.bottom_right[0]),
                       abs(self.bottom_right[1] - parent.bottom_right[1])]
