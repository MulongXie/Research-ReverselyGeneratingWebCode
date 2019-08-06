import cv2
import numpy as np

import ip_preprocessing as pre
import line
import CONFIG as cfg
import line_to_block as l2b
import code_generation as code

C = cfg.CONFIG()


org, gray = pre.read_img('input/4.png', (0, 3000))  # cut out partial img
binary = pre.preprocess(gray, 1)

# detect lines
lines_h, lines_v = line.detect_line(binary, C.LINE_MIN_LENGTH_HORIZONTAL, C.LINE_MIN_LENGTH_VERTICAL, C.LINE_MAX_THICKNESS, C.LINE_MAX_CROSS_POINT)
# divide blocks
blocks_h = l2b.divide_blocks_by_lines(lines_h, org.shape[0], C.BLOCK_MIN_HEIGHT)
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
open('output/webpage/x.html', 'w').write(html)
