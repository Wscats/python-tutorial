# encoding=utf-8
import cv2
import numpy as np
import json
# 1、图像转换为矩阵
img = cv2.imread('./img/test.jpg')
matrix = np.asarray(img)

sonStr = json.dumps(matrix, ensure_ascii=False, encoding='UTF-8') 
# 将数据保存到文件
#with open('screen.json', 'w') as json_file:
#    json_file.write(matrix)
# 2、矩阵转换为图像
# image = Image.fromarray(matrix)