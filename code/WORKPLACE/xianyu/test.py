import cv2
import numpy as np


def fill_color_diffuse_water_from_img(image, x, y, thres_up = (10, 10, 10), thres_down = (10, 10, 10), fill_color = (255,255,255)):
    """
    漫水填充：会改变图像
    """
    # 获取图片的高和宽
    h, w = image.shape[:2]

    # 创建一个h+2,w+2的遮罩层，
    # 这里需要注意，OpenCV的默认规定，
    # 遮罩层的shape必须是h+2，w+2并且必须是单通道8位，具体原因我也不是很清楚。
    mask = np.zeros([h + 2, w + 2], np.uint8)

    # 这里执行漫水填充，参数代表：
    # copyImg：要填充的图片
    # mask：遮罩层
    # (x, y)：开始填充的位置（开始的种子点）
    # (255, 255, 255)：填充的值，这里填充成白色
    # (100,100,100)：开始的种子点与整个图像的像素值的最大的负差值
    # (50,50,50)：开始的种子点与整个图像的像素值的最大的正差值
    # cv.FLOODFILL_FIXED_RANGE：处理图像的方法，一般处理彩色图象用这个方法
    cv2.floodFill(image, mask, (x, y), fill_color, thres_down, thres_up, cv2.FLOODFILL_FIXED_RANGE)
    cv2.imshow("a", image)
    cv2.waitKey()
    return image, mask


img = cv2.imread('E:\\Mulong\\Datasets\\rico\\combined\\10776.jpg')
img = cv2.resize(img, (int(img.shape[1]/2), int(img.shape[0]/2)))
img = cv2.GaussianBlur(img, (3,3), 0)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
lap = cv2.Laplacian(gray, cv2.CV_8U, 5)
filled, mask =  fill_color_diffuse_water_from_img(lap, 0,0)

cv2.imshow('mask', mask)
cv2.waitKey()