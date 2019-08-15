import pytesseract as pyt
import cv2

img = cv2.imread('input/g.png')
# img = cv2.resize(img, (600, 400))
org = img.copy()
data = pyt.image_to_data(img)
data = data.split('\n')

print(data[0])
for d in data[1:]:
    d = d.split()
    if d[-1] != '-1':
        if d[-1] != '-' and d[-1] != '—' and int(d[-3]) < 40:
            print(d)
            t_l = (int(d[-6]), int(d[-5]))
            b_r = (int(d[-6]) + int(d[-4]), int(d[-5]) + int(d[-3]))
            cv2.rectangle(org, t_l, b_r, (255,0,255), 1)

cv2.imshow('output', org)
cv2.waitKey(0)