import cv2
import numpy as np
from random import randint as rint


broad = np.zeros((300, 300), dtype=np.uint8)
cv2.rectangle(broad, (100, 100), (200, 200), (255, 255, 255), thickness=-1)
cv2.rectangle(broad, (120, 100), (180, 150), (0,0,0), thickness=-1)


cv2.imshow('rec', broad)
cv2.waitKey()
cv2.imwrite('dent.png', broad)


