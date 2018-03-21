# encoding=utf-8
import cv2
import numpy as np
from json import dumps
# 图片路径
IMAGE_NAME = "./img/screen.png"
# 保存为的json文件
JSON_NAME = 'screen.json'
img = cv2.imread(IMAGE_NAME)

# numpy中ndarray文件转为list
# img_list = img.tolist()
img_list = img[:,:,::-1].tolist()
# print(img_list)
# 字典形式保存数组
img_dict = {}
img_dict['name'] = IMAGE_NAME
img_dict['content'] = img_list

# 保存为json格式
# json_data = dumps(img_dict, indent=2)
json_data = dumps(img_dict)

# 将数据保存到文件
with open(JSON_NAME, 'w') as json_file:
    json_file.write(json_data)
