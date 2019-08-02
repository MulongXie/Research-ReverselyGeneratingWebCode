import pytesseract as pyt
import cv2

img = cv2.imread('8.png')
data = pyt.image_to_data(img)
data = data.split('\n')

print(data[0])
for d in data[1:]:
    d = d.split()
    if d[-1] != '-1':
        if int(d[-2]) > 80 and d[-1] != '-' and d[-1] != '—':
            print(d)
            t_l = (int(d[-6]), int(d[-5]))
            b_r = (int(d[-6]) + int(d[-4]), int(d[-5]) + int(d[-3]))
            cv2.rectangle(img, t_l, b_r, (0,0,255), 1)

cv2.imshow('ocr', img)
cv2.waitKey(0)