import cv2
import numpy as np


mask = np.full((200, 200, 3), 255, np.uint8)

cv2.imshow('img', mask)
cv2.waitKey(0)