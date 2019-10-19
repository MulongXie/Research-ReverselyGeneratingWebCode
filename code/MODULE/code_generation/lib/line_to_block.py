import pandas as pd
import cv2
import numpy as np

from BLOCK import BLOCK as B


def draw_blocks(img, blocks, hierarchy, output):
    c = 0
    bin = 256 * 3 / len(blocks)
    color = [255, 255, 255]
    for i, hier in enumerate(hierarchy):
        blocks[hier[0]].draw_block(img, color, -1, True, output + str(i) + '.png')
        color[c] -= bin
        if color[c] < 0:
            c = (c+1)%3
            color[c] = 255


# clean those lines so close to others that can be treated as the part of other line
def merge_close_lines(lines):
    # merge list members that are closer than the threshold
    def tight_set(list, thresh):
        index_row = [i[0] for i in list]
        index_row = sorted(index_row)
        list_tight = [list[0]]
        anchor = 0
        mark = anchor
        for i in range(1, len(index_row)):
            if index_row[i] - index_row[mark] <= thresh:
                mark = i
                continue
            else:
                list_tight.append(list[i])
                anchor = i
                mark = anchor
        return list_tight

    # check if there is any existing approximate range of line (column of head to column of end)
    def approximate_range(range, ranges, thresh=5):
        for r in ranges:
            if abs(range[0] - r[0]) + abs(range[1] - r[1]) < thresh:
                return r
        return -1

    # group lines in {'[range of column]': (row index, line index)}
    lines_formatted = {}
    for i, line in enumerate(lines):
        pos = (line[0][0], line[1][0])
        key = approximate_range(pos, lines_formatted.keys())
        # no approximate range existing
        if key == -1:
            if pos not in lines_formatted:
                lines_formatted[pos] = [(line[0][1], i)]
            else:
                lines_formatted[pos].append((line[0][1], i))
        else:
            lines_formatted[key].append((line[0][1], i))

    lines_merged = []
    for r in lines_formatted:
        for l in [lines[t[1]] for t in tight_set(lines_formatted[r], 3)]:
            lines_merged.append(l)
    return lines_merged


# @lines: [(head, end)] -> [((col, row), (col, row))]
# @axi = 0 divide horizontally
# @axi = 1 divide vertically
def divide_blocks_by_lines(lines, height, min_block_height):

    # package blocks according to the upper and lower bounds
    # @lines: [(head, end)] -> [((col, row), (col, row))]
    # @upper: upper bound row index for each line [row, row, row]
    def package_block(lines, upper, lower):
        index = 0
        mark = []
        blocks = []  # [(top_left, bottom_right)] -> [((column, row), (column, row)]
        for i, line in enumerate(lines):
            if lower[i] - line[0][1] > min_block_height:
                t_l = line[0]
                b_r = (line[1][0], lower[i])
                blocks.append(B(index, t_l, b_r))
                mark.append((t_l, b_r))
                index += 1

        for i, line in enumerate(lines):
            if line[0][1] - upper[i] > min_block_height:
                t_l = (line[0][0], upper[i])
                b_r = line[1]
                if (t_l, b_r) not in mark:
                    blocks.append(B(index, t_l, b_r))
                    mark.append((t_l, b_r))
                    index += 1
        return blocks

    lines = merge_close_lines(lines)
    upper = np.zeros(len(lines), dtype=int)  # y of upper bound for each line
    lower = np.full(len(lines), height)  # y of lower bound for each line

    for i in range(len(lines)):
        for j in range(len(lines)):
            if i == j:
                continue
            head_i, end_i = lines[i][0], lines[i][1]
            head_j, end_j = lines[j][0], lines[j][1]
            if not ((head_i[0] <= head_j[0] and end_i[0] > end_j[0]) or (head_i[0] < head_j[0] and end_i[0] >= end_j[0])):
                if head_i[1] > head_j[1] > upper[i]:
                    upper[i] = head_j[1]
                if head_i[1] < head_j[1] < lower[i]:
                    lower[i] = head_j[1]

    # [(top_left, bottom_right)] -> [((col, row), (col, row))]
    blocks = package_block(lines, upper, lower)
    print('*** Number of Blocks: %d ***' % len(blocks))
    return blocks


# @blocks: [(top_left, bottom_right)] -> [((col, row), (col, row))]
# @is_sored: if true, sorted by hierarchy and return list of tuples -> [(id, hierarchy)]
def hierarchical_blocks(blocks, is_sorted=True):

    for i in range(len(blocks)):
        for j in range(len(blocks)):
            if i == j:
                continue
            h = blocks[i].hierarchy(blocks[j])
            if h == 1:
                if blocks[i].child is None:
                    blocks[i].child = [blocks[j]]
                else:
                    blocks[i].child.append([blocks[j]])
            elif h == -1:
                if blocks[i].parent is None or blocks[i].parent > blocks[j]:
                    blocks[i].parent = blocks[j]

    leaves = []
    for block in blocks:
        if block.child is None:
            leaves.append(block.id)

    hierarchies = np.zeros(len(blocks), dtype=int)  # layer
    cur = leaves
    parents = []
    layer = 0
    while len(cur) > 0:
        for i in cur:
            blocks[i].layer = hierarchies[i]
            if blocks[i].parent is not None:
                parents.append(blocks[i].parent.id)
                layer = max(hierarchies[blocks[i].id], 0)
                # calculate the 'margin' attribute according to the relative position to its parent
                blocks[i].get_relative_position()
        # remove redundancy
        parents = list(set(parents))
        for i in parents:
            hierarchies[i] = layer + 1

        cur = parents
        parents = []

    if is_sorted:
        hierarchies = [(id, hierarchies[id]) for id in range(len(hierarchies))]
        hierarchies.sort(key=lambda x: x[1], reverse=True)

    return hierarchies