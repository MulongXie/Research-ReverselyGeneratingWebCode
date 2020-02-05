import xml.etree.ElementTree as et
import cv2


def draw_bounding_box(org, corners, color=(0, 255, 0), line=1, show=False):
    board = org.copy()
    for i in range(len(corners)):
        board = cv2.rectangle(board, corners[i][0], corners[i][1], color, line)
    if show:
        cv2.imshow('a', board)
        cv2.waitKey(0)
    return board


tree = et.parse('a.xml')
root = tree.getroot()
xmlns = '{http://schemas.android.com/apk/res/android}'
corners = []
for child in root:
    if child.tag != 'FrameLayout':
        attrib = child.attrib
        up_left = (int(attrib['{}layout_marginLeft'.format(xmlns)].split('.')[0]),
                   int(attrib['{}layout_marginTop'.format(xmlns)].split('.')[0]))
        bottom_right = (up_left[0] + int(attrib['{}layout_width'.format(xmlns)].split('.')[0]),
                        up_left[1] + int(attrib['{}layout_height'.format(xmlns)].split('.')[0]))

        corners.append((up_left, bottom_right))

img = cv2.imread('a.png')
draw_bounding_box(img, corners, show=True)