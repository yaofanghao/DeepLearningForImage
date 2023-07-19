"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/7/13 11:04
    @Filename: my_onnx_test.py
    @Software: PyCharm     
"""

import onnx
import numpy as np
import cv2
import onnxruntime as ort

import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

# 2023.7.17
# onnxruntime 自定义类
class OnnxProcess():
    def __init__(self, **kwargs):
        self.onnx_model_name = "hrnet-pytorch.onnx"
        self.model = onnx.load(self.onnx_model_name)
        self.sess = ort.InferenceSession(self.model.SerializeToString())

def load(onnx_model_name):
    logging.info("load onnx")
    # 创建ONNX运行时
    onnx_ = OnnxProcess()
    onnx_.onnx_model_name = "hrnet-pytorch.onnx"
    onnx_.model = onnx.load(onnx_model_name)
    onnx_.sess = ort.InferenceSession(onnx_.model.SerializeToString())

    return onnx_

def onnx_predict(img_name, onnx_):
    logging.info("load image")

    image_size = 480
    # 加载并预处理输入图像
    image = cv2.imread(img_name)
    orininal_h = np.array(image).shape[0]
    orininal_w = np.array(image).shape[1]

    image = cv2.resize(image, (image_size, image_size))
    image = image.astype(np.float32) / 255.0  # 归一化到[0, 1]范围
    image = np.transpose(image, (2, 0, 1))
    image = np.expand_dims(image, axis=0)  # 添加批次维度

    # 执行推理
    logging.info("start predict")
    # input_name = sess.get_inputs()[0].name
    # output_name = sess.get_outputs()[0].name
    input_name = 'images'
    output_name = 'output'
    output = onnx_.sess.run([output_name], {input_name: image})[0]

    # 后处理输出
    output = np.squeeze(output)  # 去除批次维度
    output = np.argmax(output, axis=0)  # 获取每个像素的类别索引

    # 将输出可视化
    class_colors = [(0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128),
                       (0, 128, 128), (128, 128, 128), (64, 0, 0)] # 类别颜色映射表
    result = np.zeros((image_size, image_size, 3), dtype=np.uint8)
    for i in range(image_size):
        for j in range(image_size):
            result[i, j] = class_colors[output[i, j]]

    result = cv2.resize(result, (orininal_w, orininal_h), interpolation=cv2.INTER_LINEAR)

    # 使用addWeighted函数进行图像叠加
    # 设置叠加的权重
    alpha = 0.3  # 第一张图像的权重
    beta = 0.8  # 第二张图像的权重
    image1 = cv2.imread(img_name)
    mix = cv2.addWeighted(image1, alpha, result, beta, 0)

    logging.info("success!")
    cv2.imshow('Mix Result', mix)
    cv2.imshow('Segmentation Result', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return 1


img_name = "1.jpg"
img_name2 = "2.jpg"
onnx_model_name = "hrnet-pytorch.onnx"

onnx_ = load(onnx_model_name=onnx_model_name)
onnx_predict(img_name=img_name, onnx_=onnx_)
onnx_predict(img_name=img_name2, onnx_=onnx_)