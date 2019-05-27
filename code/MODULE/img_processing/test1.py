import cv2
import pandas as pd


def add_label(label, ix, iy, x, y, segment_no, index):
    l = {'bx': ix, 'by': iy, 'bh': int(x - ix), 'bw': int(y - iy), 'segment_no': str(segment_no)}
    label = label.append(l, ignore_index=True)
    return label


def draw_circle(event, x, y, flags, param):
    global ix, iy, label, index
    if event == cv2.EVENT_LBUTTONDOWN:
        # fetch the start points
        ix, iy = x, y
        print('start:(%d,%d)' % (ix, iy))
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        # draw the rectangle
        cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), -1)
        cv2.addWeighted(org, 0.7, img, 0.3, 0, img)
    elif event == cv2.EVENT_LBUTTONUP:
        # save the labeled area
        index += 1
        label = add_label(label, ix, iy, x, y, '0', index)
        print('end:(%d,%d) No:%d' % (x, y, index))
        print(label, '\n')


img = cv2.imread('0.png')
org = img.copy()
label = pd.read_csv('0.csv', index_col=0)
index = len(label) - 1

ix, iy = -1, -1

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_circle, [index])
while (1):
    cv2.imshow('image', img)
    k = cv2.waitKey(1)
    if k == ord('z'):
        label = label.drop(index=index)
        index -= 1
        img = org.copy()
        print('withdraw label', index)
        print(label)
    if k == ord('q'):
        break

cv2.destroyAllWindows()
label.to_csv('re.csv')
