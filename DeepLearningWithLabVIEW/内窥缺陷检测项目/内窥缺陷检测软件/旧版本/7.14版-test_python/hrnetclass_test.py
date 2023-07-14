"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/7/12 17:30
    @Filename: hrnetclass_test.py
    @Software: PyCharm     
"""
# -*- coding: utf-8 -*-

from nets.hrnet import HRnet

# 日志调试模块
import logging
# logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s %(message)s',level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


class HRNetSegmentation(object):

    def __init__(self, **kwargs):
        self.model_path = 'logs.h5'
        self.num_classes = 9  # 所需要区分的类的个数+1
        self.backbone = "hrnetv2_w32"  # 主干特征提取网络 hrnetv2_w18 hrnetv2_w32 hrnetv2_w48
        self.input_shape = [480, 480]  # 输入模型的图片尺寸
        self.colors = [(0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128),
                       (0, 128, 128), (128, 128, 128), (64, 0, 0)]

        #   加载模型
        self.model = HRnet([self.input_shape[0], self.input_shape[1], 3], self.num_classes, backbone=self.backbone)
        self.model.load_weights(self.model_path)
        logging.info('success load model: {}'.format(self.model_path))

        self.__Parameter = self.model

    # 2023.7.12 装饰器
    def GetValue(self):
        return self.__Parameter

# 2023.7.12-重写
# 包装函数
def getClassData():
    newClassObject = HRNetSegmentation()
    return newClassObject.GetValue()

print(getClassData())