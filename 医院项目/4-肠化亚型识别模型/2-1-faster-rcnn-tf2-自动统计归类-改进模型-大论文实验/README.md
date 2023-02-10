## 改进 Faster-RCNN 模型

https://blog.csdn.net/weixin_42310154/article/details/119889682
https://blog.csdn.net/weixin_44791964/article/details/108513563

可能的想法：
* 选用ResNet50替换原模型的VGG16，作为backbone
* 将relu替换为leaky relu
* 减少proposal个数 ？
  * 代码修改 nets/frcnn.py 中的 num_anchors （原的值为9，三种尺度x三种比例） 
  * 可以考虑改为4？（两种尺度x两种比例）
* 改小锚框个数
* 修改损失函数Loss？
* 加入注意力机制  
  * https://github.com/bubbliiiing/Keras-Attention
  * 代码见 nets/resent.py 中的107行
  * [1]彭伊娟,王振超,张秋菊.改进的Faster-RCNN算法在聚乙烯管接头内部缺陷检测中的应用[J/OL].应用声学:1-12.
* 优化NMS算法（加判别条件）
  在RPN产生Proposal时候为了避免重叠的候选框，以分类得分为标准，使用了NMS进行后处理。事实上，该方法对于遮挡的目标很不友好，即有可能是两个目标的Proposal很可能会被过滤掉一个，造成漏检，因此改进这个NMS模式也是可以带来检测性能提升。
* 	

## 对比实验的设计
* 大论文3.4 节 baseline模型对比
  
|  baseline模型   |   |   |
|  ----  | ----  | ---- | 
|  YOLOv3   |   |   |
|  SSD   |   |   |
|  Faster-RCNN   |   |   |


* 大论文3.5节 基于faster-rcnn的改进模型
**数据记录详见 肠化识别数据.xlsx**
* 运行summary.py可以测试模型参数、是否搭建成功

|  变量   | 对应代码修改处  | 代码是否可行  |
|  ----  | ----  | ---- | 
|  backbone选择 vgg / resnet  | 1、train.py 中第25行设置backbone的值 2、frcnn.py 中第37行设置backbone的值  | √ | 
|  激活函数选择 relu / leaky-relu  | nets/resnet.py 中将第15行 leaky_flag 设置为False/True  | √ | 
|  注意力模块选择 无 / SE-Net  | nets/resnet.py 中将第17行 attention_flag 设置为False/True | √ | 
|  正常锚框 128，256，512 -> 改小锚框 32，64，128  | train.py 中第35行设置 anchors_size 的值  | √ | 

