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

    def relation(self, bound):
        '''
        relation: -1 : a in b
                  0  : a, b are not intersected
                  1  : b in a
                  2  : a, b are identical or intersected
        '''
        col_min, row_min, col_max, row_max = bound
        bbox = Bbox(col_min, row_min, col_max, row_max)
        return self.bbox.bbox_relation_nms(bbox)

    def resize_bbox(self, det_height, tgt_height, bias):
        col_min, row_min, col_max, row_max = self.bbox.put_bbox()
        scale = tgt_height / det_height
        self.bbox = Bbox(int(col_min*scale) + bias, int(row_min*scale) + bias, int(col_max*scale) - bias, int(row_max*scale) - bias)