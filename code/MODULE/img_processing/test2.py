import cv2
import numpy as np

img = cv2.imread('0.png')
# img = np.zeros((200, 200, 3), dtype=np.uint8)
# cv2.line(img, (30, 30), (60, 60), (255, 0, 0))

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
minLineLength = 100
maxLineGap = 10
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, None, minLineLength, maxLineGap)
for line in lines:
    for x1,y1,x2,y2 in line:
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

cv2.imshow('img', img)
cv2.imshow('edge', edges)
cv2.waitKey(0)