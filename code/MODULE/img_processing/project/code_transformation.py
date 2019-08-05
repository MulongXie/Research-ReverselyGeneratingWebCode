import numpy as np


class DIV:
    def __init__(self, id):
        self.head = '<div id="' + str(id) + '">\n'
        self.body = ''
        self.tail = '</div>'
        self.code = self.head + self.body + self.tail

    def insert_body(self, div):
        self.body += '\t' + div.code + '\n'

    def merge(self):
        self.code = self.head + self.body + self.tail


def gen_html(blocks, hierarchies):
    roots = []
    leaves = []
    for block in blocks:
        if block.child is None:
            leaves.append(block.id)
        if block.parent is None:
            roots.append(block.id)
    divs = []
    for block in blocks:
        divs.append(DIV(block.id))

    cur = leaves
    parents = []

    while len(cur) > 0:
        for id in cur:
            divs[id].merge()
            if blocks[id].parent is not None:
                parent_id = blocks[id].parent.id
                divs[parent_id].insert_body(divs[id])
                parents.append(parent_id)
        # remove redundancy
        cur = list(set(parents))
        parents = []

    for r in roots:
        print(divs[r].code)