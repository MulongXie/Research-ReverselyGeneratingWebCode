import cv2
import numpy as np


broad = np.full((200, 300), 255, dtype=np.uint8)
cv2.rectangle(broad, (10, 10), (100, 100), (0), -1)

cv2.imshow('broad', broad)
cv2.waitKey()
