<!--
 * @Author: yao fanghao
 * @Date: 2023-04-16 15:01:29
 * @LastEditTime: 2023-06-19 16:39:38
 * @LastEditors: yao fanghao
-->
# 改进 Faster-RCNN 模型

<https://blog.csdn.net/weixin_42310154/article/details/119889682>
<https://blog.csdn.net/weixin_44791964/article/details/108513563>

可能的想法：

* 选用ResNet50替换原模型的VGG16，作为backbone
* 选用leaky relu替换原模型的relu
* 减少proposal个数 ？
  * 代码修改 nets/frcnn.py 中的 num_anchors （原的值为9，三种尺度x三种比例）
  * 可以考虑改为4？（两种尺度x两种比例）
* 改小锚框个数
* 修改损失函数Loss？
  * 修改为smoothl1plus
  * y = 1/log(2)*((abs(x)+1).*log(abs(x)+1)+log(2)-abs(x))
  * 其导数在-1和1处更为平滑
  * 有效降低大梯度难学样本与小梯度易学样本间的不平衡问题
* 加入注意力机制  
  * <https://github.com/bubbliiiing/Keras-Attention>
  * [1]彭伊娟,王振超,张秋菊.改进的Faster-RCNN算法在聚乙烯管接头内部缺陷检测中的应用[J/OL].应用声学:1-12.
* 优化NMS算法（加判别条件）
  在RPN产生Proposal时候为了避免重叠的候选框，以分类得分为标准，使用了NMS进行后处理。事实上，该方法对于遮挡的目标很不友好，即有可能是两个目标的Proposal很可能会被过滤掉一个，造成漏检，因此改进这个NMS模式也是可以带来检测性能提升。

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
|  优化anchor boxes设计，正常锚框 128，256，512 -> 改小锚框 32，64，128  | utils/anchors.py 中的 get_anchors()的sizes值  | √ |
|  使用类别不平衡损失函数，改进损失函数smoothl1plus  | 训练时使用train_soomthl1plus.py 替代 train.py  | 未测试 |
| 优化NMS算法，adaptive-NMS | utils/utils_bbox.py 中将第197行 non_max_suppression函数 参数根据需要配置 | 未测试 |

* adaptive-NMS
  * Adaptive NMS 是一种自适应非极大值抑制（Non-Maximum Suppression，NMS）方法，该方法可以根据不同的图片和物体计算最佳 IOU 阈值，并根据阈值自适应调整 NMS 的执行方式，从而在不同数据集和任务下获得更加准确和稳定的结果。

  具体来说，Adaptive NMS 的实现原理如下：
  1. 在训练过程中，对于每个物体，记录其与其他同类别物体的 IOU 值，然后按照 IOU 值从小到大排序。同时，记录每个物体被预测为正样本的置信度得分。
  2. 统计每个 IOU 区间内的正样本得分均值和标准差，以及 IOU 区间内样本的数量。
  3. 使用以上统计数据，计算每个 IOU 区间的目标阈值 T 和删除阈值 D，其中目标阈值 T 为正样本得分均值加上一个动态系数 k 乘以标准差，删除阈值 D 为目标阈值 T 减去一个固定衰减量 d。
  4. 对于每张测试图片，计算预测框之间的 IOU 值，并根据当前 IOU 值是否超过目标阈值 T 来决定是否保留该预测框，或者按照该预测框的得分进行排序，根据删除阈值 D 来决定保留哪些预测框。
  5. 在上述过程中，对于每个物体只保留得分最高的预测框，以便消除重复检测的问题。

  需要注意的是，Adaptive NMS 的具体实现方式可以根据实际情况进行修改和调整。比如，可以使用不同的统计方法来计算目标阈值 T 和删除阈值 D，也可以使用不同的系数和参数设置来影响模型的准确性和效率。
