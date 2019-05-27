import cv2

img = cv2.imread('bb.png')
img = cv2.blur(img, (3, 3))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
r, binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

bin, contours, hierarchy = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)  # 输出为三个参数
cv2.drawContours(img, contours, -1, (0, 0, 255), 1)

cv2.imshow('bin', bin)
cv2.imshow("img", img)
cv2.waitKey(0)
