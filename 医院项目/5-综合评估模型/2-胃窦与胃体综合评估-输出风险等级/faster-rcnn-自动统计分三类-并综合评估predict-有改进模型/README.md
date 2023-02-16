## 综合评估predict代码
2023.2.16-

* 综合评估实现逻辑
  * 输入n张胃窦图片，取其中所有图片预测结果分数最大值作为预测类别A
  * 输入m张胃体图片，取其中所有图片预测结果分数最大值作为预测类别B
  * 进入判断语句：根据A和B的值，输出对应的风险等级
    * 0-1 / 2 / high risk
    * high risk 类别是我们重点关注的，此项的准确率比较重要




* 模型训练参数可修改内容说明：
  
  |  变量   | 对应代码修改处  | 代码是否可行  |
  |  ----  | ----  | ---- | 
  |  backbone选择 vgg / resnet  | 1、train.py 中第25行设置backbone的值 2、frcnn.py 中第37行设置backbone的值  | √ | 
  |  激活函数选择 relu / leaky-relu  | nets/resnet.py 中将第15行 leaky_flag 设置为False/True  | √ | 
  |  注意力模块选择 无 / SE-Net  | nets/resnet.py 中将第17行 attention_flag 设置为False/True | √ | 
  |  正常锚框 128，256，512 -> 改小锚框 32，64，128  | utils/anchors.py 中的 get_anchors()的sizes值  | √ | 

