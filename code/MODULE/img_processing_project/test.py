import pytesseract as pyt
import cv2

img = cv2.imread('output/clean.png')

data = pyt.image_to_data(img).split('\n')
for d in data[1:]:
    d = d.split()
    if d[-1] != '-1':
        if d[-1] != '-' and d[-1] != '—' and int(d[-3]) < 40:
            t_l = (int(d[-6]), int(d[-5]))
            b_r = (int(d[-6]) + int(d[-4]), int(d[-5]) + int(d[-3]))
            cv2.rectangle(img, t_l, b_r, (0, 0, 255), 1)

cv2.imwrite('output/ocr.png', img)