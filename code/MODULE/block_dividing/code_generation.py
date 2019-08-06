import numpy as np


class DIV:
    def __init__(self, id):
        self.head = '<div id="' + str(id) + '">\n'
        self.body = ''
        self.tail = '</div>' + str(id) + '\n'
        self.code = self.head + self.body + self.tail

    def insert_body(self, code):
        self.body += code
        self.merge()

    def merge(self):
        self.code = self.head + self.body + self.tail

    def indent(self):
        head = '\t' + self.head
        if self.body is not '':
            lines = self.body.split('\n')
            lines = ['\t' + l + '\n' for l in lines]
            body = ''.join(lines)[:-1]
        else:
            body = ''
        tail = '\t' + self.tail
        code = head + body + tail
        return code


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
                divs[parent_id].insert_body(divs[id].indent())
                parents.append(parent_id)
        # remove redundancy
        cur = list(set(parents))
        parents = []

    # code = ''.join([divs[r].code for r in roots])
    print(len(roots))
    f = open('output/webpage/x.html', 'w')
    f.write(divs[roots[0]].code)