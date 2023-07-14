"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/7/12 11:06
    @Filename: 2-测试onnx模型有效性.py
    @Software: PyCharm     
"""
import onnx

# Preprocessing: load the ONNX model
model_path = 'hrnet.onnx'
onnx_model = onnx.load(model_path)
print('The model is:\n{}'.format(onnx_model))

# Check the model
try:
    onnx.checker.check_model(onnx_model)
except onnx.checker.ValidationError as e:
    print('The model is invalid: %s' % e)
else:
    print('The model is valid!')