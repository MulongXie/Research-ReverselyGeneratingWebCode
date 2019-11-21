from code_generation import DIV
import line
import line_to_block as l2b
import code_generation as code
from config import CONFIG as cfg
import ip_preprocessing as pre

C = cfg()

org, gray = pre.read_img('input/4.png', (0, 3000))  # cut out partial img

lines_v = line.read_lines('output/lines_v.csv')
lines_h = line.read_lines('output/lines_h.csv')
blocks_h = l2b.divide_blocks_by_lines(lines_h, org.shape[0], C.BLOCK_MIN_HEIGHT)
hierarchies_h = l2b.hierarchy_blocks(blocks_h)

print(hierarchies_h)

# html = code.gen_html2(blocks_h)
# open('output/y.html', 'w').write(html)

# code.gen_css(blocks_h)
