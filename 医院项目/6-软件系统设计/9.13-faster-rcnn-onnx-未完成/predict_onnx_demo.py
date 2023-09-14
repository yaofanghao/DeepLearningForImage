"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/9/14 10:53
    @Filename: predict_onnx_demo.py
    @Software: PyCharm     
"""

# import onnxruntime
# import numpy as np
# from PIL import Image
#
# # 加载ONNX模型
# model_path = 'faster_rcnn.onnx'
# session = onnxruntime.InferenceSession(model_path)
#
# # 预处理图像
# image_path = '1.jpg'
# image = Image.open(image_path).convert('RGB')
# resized_image = image.resize((600, 600))
# input_image = np.array(resized_image).astype(np.float32) / 255.0
# input_tensor = np.transpose(input_image, (2, 0, 1))
# input_tensor = np.expand_dims(input_tensor, axis=0)
#
# # 提供比例尺
# scale = 1.0  # 根据具体需求设置比例尺的值
#
# # 执行推理
# input_names = [input.name for input in session.get_inputs()]
# output_names = [output.name for output in session.get_outputs()]
# inputs = {input_names[0]: input_tensor, input_names[1]: np.array(scale).astype(np.float64)}
# outputs = session.run(output_names, inputs)
#
# # 处理预测结果
# # 根据模型的输出结构和具体任务需求，解析并处理输出结果

import onnxruntime
import numpy as np

# 加载ONNX模型
model_path = 'faster_rcnn.onnx'
session = onnxruntime.InferenceSession(model_path)

# 获取输入和输出名称
input_names = [input.name for input in session.get_inputs()]
output_names = [output.name for output in session.get_outputs()]

# 模拟特征图列表
feature_map1 = np.random.rand(3, 600, 600).astype(np.float32)  # 示例特征图1
# feature_map2 = np.random.rand(3, 600, 600).astype(np.float32)  # 示例特征图2
# feature_maps = [feature_map1, feature_map2]

# 检查特征图的维度是否匹配
num_channels = feature_maps[0].shape[0]
for i, feature_map in enumerate(feature_maps[1:], 1):
    if num_channels != feature_map.shape[0]:
        raise ValueError(f"Dimension mismatch at index {i}: {num_channels} vs {feature_map.shape[0]}")

# 执行推理
scale = 1.0
input_names = [input.name for input in session.get_inputs()]
output_names = [output.name for output in session.get_outputs()]
inputs = {input_names[0]: np.array(feature_maps), input_names[1]: np.array(scale).astype(np.float64)}
outputs = session.run(output_names, inputs)

# 处理预测结果
# 根据模型的输出结构和具体任务需求，解析并处理输出结果

