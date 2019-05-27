import cv2
import pandas as pd

drawing = False
ix, iy = -1, -1


def add_label(label, ix, iy, x, y, segment_no, index):
    l = {'bx': ix, 'by': iy, 'bh': int(x - ix), 'bw': int(y - iy), 'segment_no': str(segment_no)}
    label = label.append(l, ignore_index=True)
    return label


def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing, img_no, label
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        print('start:(%d,%d)' % (ix, iy))
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        if drawing == True:
            cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), -1)
            cv2.addWeighted(org, 0.7, img, 0.3, 0, img)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing == False
        img_no += 1

        label = add_label(label, ix, iy, x, y, '0', img_no)
        print('end:(%d,%d) No:%d' % (x, y, img_no))
        print(label, '\n')


img = cv2.imread('0.png')
org = img.copy()

label = pd.read_csv('0.csv', index_col=0)
length = len(label)
img_no = length - 1

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_circle, [label])
while (1):
    cv2.imshow('image', img)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break
    if k == ord('z'):
        label = label.drop(index=img_no)
        img_no -= 1
        img = org.copy()
        print('withdraw label', img_no)
        print(label)

cv2.destroyAllWindows()
print(label)
label.to_csv('re.csv')