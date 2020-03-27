import json

from lib_ip.Bbox import Bbox
import lib_ip.ip_draw as draw


def load_blocks(file_path):
    Blocks = []
    blocks = json.load(open(file_path, encoding='utf-8'))['blocks']
    for block in blocks:
        block = Block((block['column_min'], block['row_min'], block['column_max'], block['row_max']), block['id'], block['layer'], block['parent'])
        Blocks.append(block)
    return Blocks


class Block:
    def __init__(self, bound, id, layer, parent_id):
        col_min, row_min, col_max, row_max = bound
        self.bbox = Bbox(col_min, row_min, col_max, row_max)

        self.id = id
        self.layer = layer
        self.parent_id = parent_id

    def put_bbox(self):
        return self.bbox.put_bbox()
