"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/7/12 11:39
    @Filename: 3-onnx_summary.py
    @Software: PyCharm     
"""

# https://netron.app/
# 在线查看onnx网络模型结构图

# format ONNX v6
#
# producer pytorch 1.8
#
# imports ai.onnx v11
#
# INPUTS
# name: input1
# type: float32[1,3,480,480]
#
# OUTPUTS
# softmax
# name: softmax
# type: float32[Resizeoutput_dim_0,Resizeoutput_dim_1,Resizeoutput_dim_2,Resizeoutput_dim_3]