"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/7/24 10:42
    @Filename: test.py
    @Software: PyCharm     
"""


# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np

def readimg(image_path, output_path):
    image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
    # image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    output_image_name = image_path.rsplit("\\", 1)[-1]
    output_path_all = output_path+output_image_name

    # 处理模块，在这里进行修改
    _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

    cv2.imencode('.jpg', binary_image)[1].tofile(output_path_all)

    print("111")
    # cv2.imshow('Binary Image', binary_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return 1

# image_path="C:\\Users\\Rainy\\Desktop\\test_camera\\img\\210.jpg"
# output_path="C:\\Users\\Rainy\\Desktop\\test_camera\\img_out\\"
# readimg(image_path=image_path, output_path=output_path)
