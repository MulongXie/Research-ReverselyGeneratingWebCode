import cv2

imgs = [cv2.imread('9.png')]

c_width = 1
c_height = 0

for i, img in enumerate(imgs):
    print(img.shape)
    clip = img[c_height: 1200, c_width:-c_width]
    cv2.imwrite(str(i) + '.png', clip)