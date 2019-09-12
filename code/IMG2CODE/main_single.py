import merge
import ocr
import ui

from file_utils import time_start, timer_end


PATH_IMG_INPUT = 'data/input/282.png'
PATH_LABEL_COMPO = 'data/output/compo.json'
PATH_LABEL_TEXT = 'data/output/ocr.txt'
PATH_CTPN_DRAWN_OUTPUT = 'data/output/ctpn.png'
PATH_UIED_DRAWN_OUTPUT = 'data/output/uied.png'
PATH_UIED_BIN_OUTPUT = 'data/output/gradient.png'
PATH_MERGE_OUTPUT = 'data/output/merged.png'

start = time_start()

ocr.ctpn(PATH_IMG_INPUT, PATH_LABEL_TEXT, PATH_CTPN_DRAWN_OUTPUT)
ui.uied(PATH_IMG_INPUT, PATH_LABEL_COMPO, PATH_UIED_DRAWN_OUTPUT, PATH_UIED_BIN_OUTPUT)
merge.incorporate(PATH_IMG_INPUT, PATH_LABEL_COMPO, PATH_LABEL_TEXT, PATH_MERGE_OUTPUT)

timer_end(start)
