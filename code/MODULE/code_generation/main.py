import cv2
import numpy as np
import time

import ip_preprocessing as pre
import line
from config import CONFIG as cfg
import line_to_block as l2b
import code_generation as code

start = time.clock()
C = cfg()
is_line = False
is_block = True
is_code = True

org, gray = pre.read_img('input/4.png', (0, 3000))  # cut out partial img
binary = pre.preprocess(gray, 1)

# detect lines
if is_line:
    lines_h, lines_v = line.detect_line(binary, C.LINE_MIN_LENGTH_HORIZONTAL, C.LINE_MIN_LENGTH_VERTICAL, C.LINE_MAX_THICKNESS, C.LINE_MAX_CROSS_POINT)
    line.save_lines('output/lines_v.csv', lines_v)
    line.save_lines('output/lines_h.csv', lines_h)
else:
    lines_v = line.read_lines('output/lines_v.csv')
    lines_h = line.read_lines('output/lines_h.csv')

# divide blocks
if is_block:
    blocks_h = l2b.divide_blocks_by_lines(lines_h, org.shape[0], C.BLOCK_MIN_HEIGHT)

if is_code:
    # calculate the hierarchy among blocks
    hierarchies_h = l2b.hierarchical_blocks(blocks_h)
    # generate code according to hierarchy
    html = code.gen_html(blocks_h, hierarchies_h)


# save results
broad_line = np.zeros(org.shape, dtype=np.uint8)
broad_block = np.zeros(org.shape, dtype=np.uint8)
line.draw_line(broad_line, lines_h, (0, 255, 0))
line.draw_line(broad_line, lines_v, (0, 0, 255))

l2b.draw_blocks(broad_block, blocks_h, hierarchies_h, 'output/blocks/')
cv2.imwrite('output/line.png', broad_line)
cv2.imwrite('output/grad.png', binary)
cv2.imwrite('output/org.png', org)
open('output/x.html', 'w').write(html)

print('*** Time:%.3f ***' %(time.clock() - start))
