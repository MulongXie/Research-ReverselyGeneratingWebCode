import cv2
import numpy as np


def nothing(x):
    pass


name = '10'
img = cv2.imread(name + '.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

og = cv2.imread('ours_grad/' + name + '.png')
ot = cv2.imread('ours_outcome/' + name + '.png')

cv2.namedWindow('img')
cv2.namedWindow("control")
cv2.createTrackbar("lowc", "control", 0, 1000, nothing)
cv2.createTrackbar("highc", "control", 0, 1000, nothing)
cv2.createTrackbar("lowt", "control", 0, 255, nothing)
cv2.createTrackbar("hight", "control", 0, 255, nothing)
cv2.createTrackbar("image_select", "control", 0, 3, nothing)

while True:
    lowc = cv2.getTrackbarPos('lowc', 'control')  # 100,300
    highc = cv2.getTrackbarPos('highc', 'control')
    can = cv2.Canny(gray, lowc, highc)

    lwot = cv2.getTrackbarPos('lowt', 'control')
    hight = cv2.getTrackbarPos('hight', 'control')
    ret, binary = cv2.threshold(gray, lwot, hight, cv2.THRESH_BINARY)
    _, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    con = np.zeros(img.shape[:3], dtype=np.uint8)
    cv2.drawContours(con, contours, -1, (0, 0, 255), 1)

    flag = cv2.getTrackbarPos('image_select', 'control')
    if flag == 0:
        cv2.imshow("img", can)
    elif flag == 1:
        cv2.imshow("img", con)
    elif flag == 2:
        cv2.imshow("img", og)
    elif flag == 3:
        cv2.imshow("img", ot)

    key = cv2.waitKey(10)
    if key == ord('q'):
        cv2.imwrite('canny.png', can)
        cv2.imwrite('contour.png', con)
        break




