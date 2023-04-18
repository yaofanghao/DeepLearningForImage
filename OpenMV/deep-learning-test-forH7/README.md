"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/4/18 16:10
    @Filename: README.md.py
    @Software: PyCharm     
"""

# 深度学习示例-图像分类
* 参考资料
  * https://singtown.com/learn/50872/
  * https://github.com/SingTown/mask-tflite
  * https://blog.csdn.net/qingchedeyongqi/article/details/119254988
  * 

# 实现流程
* 新建数据集文件夹 dataset
* 拍摄照片，制作数据集
  * 分辨率选择QQVGA 
* edge impluse 平台训练模型
  * 不推荐用API keys上传
  * impulse-design 图像预处，按步骤进行即可
  * 采用 MobileNetV2 96x96 0.35 (final layer: 16 neurons, 0.1 dropout)
  * 运行完成最终能生成 TF-Lite int8 quantized model
  * 并可查看模型推理时间、占用Flash存储大小等信息
* deploy模型，部署到本地
  * 生成模型625K，不可用于H7

## 改进：获取小模型的方法
* 不要选择默认的transfer learning模型
* 选择keras那一项模型
* 然后可以在classifier中，自定义组合网络结构
  * 这里选用的网络结构参考 train_mode_2.py
  * 2D conv / pool layer (32 filters, 3 kernel size, 1 layer)
  * 2D conv / pool layer (16 filters, 3 kernel size, 1 layer)
  * Flatten layer
  * Dropout (rate 0.25)
  * Output layer (2 classes)
* deploy模型，部署到本地
  * 生成模型30K
