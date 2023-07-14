"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/7/12 11:22
    @Filename: 4-使用我的onnx模型推理测试.py
    @Software: PyCharm     
"""

# hrnet.onnx 模型推理，输入图片480x480x3，输出480x480x9

import onnx
import numpy as np
import cv2
import copy

import logging
# logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s %(message)s',level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

logging.info("load onnx")

# 加载ONNX模型
onnx_model = onnx.load('deeplabv3_resnet101.onnx')
image_size = 448

# 创建ONNX运行时
import onnxruntime as ort
sess = ort.InferenceSession(onnx_model.SerializeToString())

logging.info("load image")

# 加载并预处理输入图像
image = cv2.imread('1.jpg')

#   对输入图像进行一个备份，后面用于绘图
old_img = copy.deepcopy(image)
orininal_h = np.array(image).shape[0]
orininal_w = np.array(image).shape[1]

image = cv2.resize(image, (image_size, image_size))  # 调整图像大小为480x480
image = image.astype(np.float32) / 255.0  # 归一化到[0, 1]范围
# image = np.transpose(image, (2, 0, 1))  # 改变维度顺序为(3, 480, 480)
image = np.expand_dims(image, axis=0)  # 添加批次维度

logging.info("start predict")

# 执行推理
input_name = sess.get_inputs()[0].name
output_name = sess.get_outputs()[0].name
output = sess.run([output_name], {input_name: image})[0]

# 后处理输出
output = np.squeeze(output)  # 去除批次维度
output = np.argmax(output, axis=2)  # 获取每个像素的类别索引

# 可选：将输出可视化
class_colors = [(0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128),
                       (0, 128, 128), (128, 128, 128), (64, 0, 0)]  # 类别颜色映射表
result = np.zeros((image_size, image_size, 3), dtype=np.uint8)
for i in range(image_size):
    for j in range(image_size):
        result[i, j] = class_colors[output[i, j]]

result = cv2.resize(result, (orininal_w, orininal_h), interpolation=cv2.INTER_LINEAR)

logging.info("success!")


cv2.imshow('Segmentation Result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()

