import json
from lib_ip.Bbox import Bbox


def load_tree(file_path):
    root = json.load(open(file_path, encoding="utf8"))


class Tree:
    def __init__(self, bound, class_name, children):
        col_min, row_min, col_max, row_max = bound
        self.bbox = Bbox(col_min, row_min, col_max, row_max)

        self.class_name = class_name
        self.children = children

