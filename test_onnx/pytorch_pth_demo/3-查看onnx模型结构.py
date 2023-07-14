"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/7/12 11:39
    @Filename: 3-查看onnx模型结构.py
    @Software: PyCharm     
"""

# https://netron.app/
# 在线查看onnx网络模型结构图

# format ONNX v6
#
# producer tf2onnx 1.14.0 8f8d49
#
# imports ai.onnx v11 ai.onnx.ml v2
#
# description converted from ./_hrnet
#
# input_1
# name: input_1
# type: float32[unk__4478,480,480,3]
#
# OUTPUTS
# softmax
# name: softmax
# type: float32[unk__4479,480,480,9]