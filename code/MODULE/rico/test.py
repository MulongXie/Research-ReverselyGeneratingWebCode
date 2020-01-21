import cv2
import numpy as np

board = np.zeros((500, 500), dtype=np.uint8)

cv2.rectangle(board, (10,10), (110, 10 + int(100/40)), (255), 1)
cv2.imshow('o', board)
cv2.waitKey()