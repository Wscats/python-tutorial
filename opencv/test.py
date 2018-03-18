# encoding=utf-8
import cv2 as cv2
import numpy as np
img = cv2.imread("img/test.jpg")
# cv2.imshow("lena",img)
# cv2.waitKey(10000)
cv2.namedWindow("Image")  # 初始化一个名为Image的窗口
cv2.imshow("Image", img)  # 显示图片
cv2.waitKey(0)  # 等待键盘触发事件，释放窗口