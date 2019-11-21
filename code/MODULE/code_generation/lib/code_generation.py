import numpy as np


class DIV:
    def __init__(self, id):
        self.head = '<div id="' + str(id) + '">\n'
        self.body = ''
        self.tail = '</div>\n'
        self.code = self.head + self.body + self.tail

    def insert_body(self, code):
        self.body += code
        self.assemble_code()

    def assemble_code(self):
        self.code = self.head + self.body + self.tail

    def indent(self):
        head = '\t' + self.head
        lines = self.body.split('\n')
        lines = ['\t' + l + '\n' for l in lines]
        body = ''.join(lines)[:-1]
        tail = self.tail
        code = head + body + tail
        return code


def gen_html(blocks, hierarchies):
    roots = []
    leaves = []
    for block in blocks:
        if block.children is None:
            leaves.append(block.id)
        if block.parent is None:
            roots.append(block.id)
    divs = []
    for block in blocks:
        divs.append(DIV(block.id))

    cur = leaves
    parents = []

    while len(cur) > 0:
        print(cur)
        for id in cur:
            divs[id].assemble_code()
            if blocks[id].parent is not None:
                parent_id = blocks[id].parent.id
                divs[parent_id].insert_body(divs[id].indent())
                if parent_id not in parents:
                    parents.append(parent_id)
        # remove redundancy
        cur = parents
        parents = []

    html = ''.join([divs[r].code for r in roots])
    return html


def gen_html2(blocks):

    def fetch_child(block):
        div = DIV(block.id)
        if block.children is not None:
            for child in block.children:
                div.insert_body(fetch_child(child).indent())
        return div

    root_blocks = []
    for b in blocks:
        if b.parent is None:
            root_blocks.append(b)

    html = ''
    for root in root_blocks:
        html += fetch_child(root).code
    return html


def gen_css(blocks):
    for block in blocks:
        print(block.margin)