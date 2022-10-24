from functools import wraps

from tensorflow.keras.initializers import RandomNormal
from tensorflow.keras.layers import (BatchNormalization, Concatenate, Conv2D,
                                     Input, Lambda, LeakyReLU, UpSampling2D)
from tensorflow.keras.models import Model
from tensorflow.keras.regularizers import l2
# from utils import compose
from functools import reduce
from functools import partial
from tensorflow.keras import backend as K

# from efficientnet import (EfficientNetB0, EfficientNetB1, EfficientNetB2,
#                                EfficientNetB3, EfficientNetB4, EfficientNetB5,
#                                EfficientNetB6, EfficientNetB7)
# from yolo_training import yolo_loss

## 7.23 额外添加的
###########################
def compose(*funcs):
    if funcs:
        return reduce(lambda f, g: lambda *a, **kw: g(f(*a, **kw)), funcs)
    else:
        raise ValueError('Composition of empty sequence not supported.')


import math
from copy import deepcopy

import tensorflow as tf
from tensorflow.keras import backend, layers


# ---------------------------------------------------#
#   对box进行调整，使其符合真实图片的样子
# ---------------------------------------------------#
def yolo_correct_boxes(box_xy, box_wh, input_shape, image_shape, letterbox_image):
    # -----------------------------------------------------------------#
    #   把y轴放前面是因为方便预测框和图像的宽高进行相乘
    # -----------------------------------------------------------------#
    box_yx = box_xy[..., ::-1]
    box_hw = box_wh[..., ::-1]
    input_shape = K.cast(input_shape, K.dtype(box_yx))
    image_shape = K.cast(image_shape, K.dtype(box_yx))

    if letterbox_image:
        # -----------------------------------------------------------------#
        #   这里求出来的offset是图像有效区域相对于图像左上角的偏移情况
        #   new_shape指的是宽高缩放情况
        # -----------------------------------------------------------------#
        new_shape = K.round(image_shape * K.min(input_shape / image_shape))
        offset = (input_shape - new_shape) / 2. / input_shape
        scale = input_shape / new_shape

        box_yx = (box_yx - offset) * scale
        box_hw *= scale

    box_mins = box_yx - (box_hw / 2.)
    box_maxes = box_yx + (box_hw / 2.)
    boxes = K.concatenate([box_mins[..., 0:1], box_mins[..., 1:2], box_maxes[..., 0:1], box_maxes[..., 1:2]])
    boxes *= K.concatenate([image_shape, image_shape])
    return boxes


# ---------------------------------------------------#
#   将预测值的每个特征层调成真实值
# ---------------------------------------------------#
def get_anchors_and_decode(feats, anchors, num_classes, input_shape, calc_loss=False):
    num_anchors = len(anchors)
    # ------------------------------------------#
    #   grid_shape指的是特征层的高和宽
    # ------------------------------------------#
    grid_shape = K.shape(feats)[1:3]
    # --------------------------------------------------------------------#
    #   获得各个特征点的坐标信息。生成的shape为(13, 13, num_anchors, 2)
    # --------------------------------------------------------------------#
    grid_x = K.tile(K.reshape(K.arange(0, stop=grid_shape[1]), [1, -1, 1, 1]), [grid_shape[0], 1, num_anchors, 1])
    grid_y = K.tile(K.reshape(K.arange(0, stop=grid_shape[0]), [-1, 1, 1, 1]), [1, grid_shape[1], num_anchors, 1])
    grid = K.cast(K.concatenate([grid_x, grid_y]), K.dtype(feats))
    # ---------------------------------------------------------------#
    #   将先验框进行拓展，生成的shape为(13, 13, num_anchors, 2)
    # ---------------------------------------------------------------#
    anchors_tensor = K.reshape(K.constant(anchors), [1, 1, num_anchors, 2])
    anchors_tensor = K.tile(anchors_tensor, [grid_shape[0], grid_shape[1], 1, 1])

    # ---------------------------------------------------#
    #   将预测结果调整成(batch_size,13,13,3,85)
    #   85可拆分成4 + 1 + 80
    #   4代表的是中心宽高的调整参数
    #   1代表的是框的置信度
    #   80代表的是种类的置信度
    # ---------------------------------------------------#
    feats = K.reshape(feats, [-1, grid_shape[0], grid_shape[1], num_anchors, num_classes + 5])
    # ------------------------------------------#
    #   对先验框进行解码，并进行归一化
    # ------------------------------------------#
    box_xy = (K.sigmoid(feats[..., :2]) + grid) / K.cast(grid_shape[::-1], K.dtype(feats))
    box_wh = K.exp(feats[..., 2:4]) * anchors_tensor / K.cast(input_shape[::-1], K.dtype(feats))
    # ------------------------------------------#
    #   获得预测框的置信度
    # ------------------------------------------#
    box_confidence = K.sigmoid(feats[..., 4:5])
    box_class_probs = K.sigmoid(feats[..., 5:])

    # ---------------------------------------------------------------------#
    #   在计算loss的时候返回grid, feats, box_xy, box_wh
    #   在预测的时候返回box_xy, box_wh, box_confidence, box_class_probs
    # ---------------------------------------------------------------------#
    if calc_loss == True:
        return grid, feats, box_xy, box_wh
    return box_xy, box_wh, box_confidence, box_class_probs


# ---------------------------------------------------#
#   图片预测
# ---------------------------------------------------#
def DecodeBox(outputs,
              anchors,
              num_classes,
              input_shape,
              # -----------------------------------------------------------#
              #   13x13的特征层对应的anchor是[116,90],[156,198],[373,326]
              #   26x26的特征层对应的anchor是[30,61],[62,45],[59,119]
              #   52x52的特征层对应的anchor是[10,13],[16,30],[33,23]
              # -----------------------------------------------------------#
              anchor_mask=[[6, 7, 8], [3, 4, 5], [0, 1, 2]],
              max_boxes=100,
              confidence=0.5,
              nms_iou=0.3,
              letterbox_image=True):
    image_shape = K.reshape(outputs[-1], [-1])

    box_xy = []
    box_wh = []
    box_confidence = []
    box_class_probs = []
    for i in range(len(anchor_mask)):
        sub_box_xy, sub_box_wh, sub_box_confidence, sub_box_class_probs = \
            get_anchors_and_decode(outputs[i], anchors[anchor_mask[i]], num_classes, input_shape)
        box_xy.append(K.reshape(sub_box_xy, [-1, 2]))
        box_wh.append(K.reshape(sub_box_wh, [-1, 2]))
        box_confidence.append(K.reshape(sub_box_confidence, [-1, 1]))
        box_class_probs.append(K.reshape(sub_box_class_probs, [-1, num_classes]))
    box_xy = K.concatenate(box_xy, axis=0)
    box_wh = K.concatenate(box_wh, axis=0)
    box_confidence = K.concatenate(box_confidence, axis=0)
    box_class_probs = K.concatenate(box_class_probs, axis=0)

    # ------------------------------------------------------------------------------------------------------------#
    #   在图像传入网络预测前会进行letterbox_image给图像周围添加灰条，因此生成的box_xy, box_wh是相对于有灰条的图像的
    #   我们需要对其进行修改，去除灰条的部分。 将box_xy、和box_wh调节成y_min,y_max,xmin,xmax
    #   如果没有使用letterbox_image也需要将归一化后的box_xy, box_wh调整成相对于原图大小的
    # ------------------------------------------------------------------------------------------------------------#
    boxes = yolo_correct_boxes(box_xy, box_wh, input_shape, image_shape, letterbox_image)

    box_scores = box_confidence * box_class_probs

    # -----------------------------------------------------------#
    #   判断得分是否大于score_threshold
    # -----------------------------------------------------------#
    mask = box_scores >= confidence
    max_boxes_tensor = K.constant(max_boxes, dtype='int32')
    boxes_out = []
    scores_out = []
    classes_out = []
    for c in range(num_classes):
        # -----------------------------------------------------------#
        #   取出所有box_scores >= score_threshold的框，和成绩
        # -----------------------------------------------------------#
        class_boxes = tf.boolean_mask(boxes, mask[:, c])
        class_box_scores = tf.boolean_mask(box_scores[:, c], mask[:, c])

        # -----------------------------------------------------------#
        #   非极大抑制
        #   保留一定区域内得分最大的框
        # -----------------------------------------------------------#
        nms_index = tf.image.non_max_suppression(class_boxes, class_box_scores, max_boxes_tensor, iou_threshold=nms_iou)

        # -----------------------------------------------------------#
        #   获取非极大抑制后的结果
        #   下列三个分别是：框的位置，得分与种类
        # -----------------------------------------------------------#
        class_boxes = K.gather(class_boxes, nms_index)
        class_box_scores = K.gather(class_box_scores, nms_index)
        classes = K.ones_like(class_box_scores, 'int32') * c

        boxes_out.append(class_boxes)
        scores_out.append(class_box_scores)
        classes_out.append(classes)
    boxes_out = K.concatenate(boxes_out, axis=0)
    scores_out = K.concatenate(scores_out, axis=0)
    classes_out = K.concatenate(classes_out, axis=0)

    return boxes_out, scores_out, classes_out


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np


    def sigmoid(x):
        s = 1 / (1 + np.exp(-x))
        return s


    # ---------------------------------------------------#
    #   将预测值的每个特征层调成真实值
    # ---------------------------------------------------#
    def get_anchors_and_decode(feats, anchors, num_classes):
        # feats     [batch_size, 13, 13, 3 * (5 + num_classes)]
        # anchors   [3, 2]
        # num_classes
        # 3
        num_anchors = len(anchors)
        # ------------------------------------------#
        #   grid_shape指的是特征层的高和宽
        #   grid_shape [13, 13]
        # ------------------------------------------#
        grid_shape = np.shape(feats)[1:3]
        # --------------------------------------------------------------------#
        #   获得各个特征点的坐标信息。生成的shape为(13, 13, num_anchors, 2)
        #   grid_x [13, 13, 3, 1]
        #   grid_y [13, 13, 3, 1]
        #   grid   [13, 13, 3, 2]
        # --------------------------------------------------------------------#
        grid_x = np.tile(np.reshape(np.arange(0, stop=grid_shape[1]), [1, -1, 1, 1]),
                         [grid_shape[0], 1, num_anchors, 1])
        grid_y = np.tile(np.reshape(np.arange(0, stop=grid_shape[0]), [-1, 1, 1, 1]),
                         [1, grid_shape[1], num_anchors, 1])
        grid = np.concatenate([grid_x, grid_y], -1)
        # ---------------------------------------------------------------#
        #   将先验框进行拓展，生成的shape为(13, 13, num_anchors, 2)
        #   [1, 1, 3, 2]
        #   [13, 13, 3, 2]
        # ---------------------------------------------------------------#
        anchors_tensor = np.reshape(anchors, [1, 1, num_anchors, 2])
        anchors_tensor = np.tile(anchors_tensor, [grid_shape[0], grid_shape[1], 1, 1])

        # ---------------------------------------------------#
        #   将预测结果调整成(batch_size,13,13,3,85)
        #   85可拆分成4 + 1 + 80
        #   4代表的是中心宽高的调整参数
        #   1代表的是框的置信度
        #   80代表的是种类的置信度
        #   [batch_size, 13, 13, 3 * (5 + num_classes)]
        #   [batch_size, 13, 13, 3, 5 + num_classes]
        # ---------------------------------------------------#
        feats = np.reshape(feats, [-1, grid_shape[0], grid_shape[1], num_anchors, num_classes + 5])
        # ------------------------------------------#
        #   对先验框进行解码，并进行归一化
        # ------------------------------------------#
        box_xy = sigmoid(feats[..., :2]) + grid
        box_wh = np.exp(feats[..., 2:4]) * anchors_tensor
        # ------------------------------------------#
        #   获得预测框的置信度
        # ------------------------------------------#
        box_confidence = sigmoid(feats[..., 4:5])
        box_class_probs = sigmoid(feats[..., 5:])

        box_wh = box_wh / 32
        anchors_tensor = anchors_tensor / 32
        fig = plt.figure()
        ax = fig.add_subplot(121)
        plt.ylim(-2, 15)
        plt.xlim(-2, 15)
        plt.scatter(grid_x, grid_y)
        plt.scatter(5, 5, c='black')
        plt.gca().invert_yaxis()

        anchor_left = grid_x - anchors_tensor / 2
        anchor_top = grid_y - anchors_tensor / 2
        print(np.shape(anchors_tensor))
        print(np.shape(box_xy))
        rect1 = plt.Rectangle([anchor_left[5, 5, 0, 0], anchor_top[5, 5, 0, 1]], anchors_tensor[0, 0, 0, 0],
                              anchors_tensor[0, 0, 0, 1], color="r", fill=False)
        rect2 = plt.Rectangle([anchor_left[5, 5, 1, 0], anchor_top[5, 5, 1, 1]], anchors_tensor[0, 0, 1, 0],
                              anchors_tensor[0, 0, 1, 1], color="r", fill=False)
        rect3 = plt.Rectangle([anchor_left[5, 5, 2, 0], anchor_top[5, 5, 2, 1]], anchors_tensor[0, 0, 2, 0],
                              anchors_tensor[0, 0, 2, 1], color="r", fill=False)

        ax.add_patch(rect1)
        ax.add_patch(rect2)
        ax.add_patch(rect3)

        ax = fig.add_subplot(122)
        plt.ylim(-2, 15)
        plt.xlim(-2, 15)
        plt.scatter(grid_x, grid_y)
        plt.scatter(5, 5, c='black')
        plt.scatter(box_xy[0, 5, 5, :, 0], box_xy[0, 5, 5, :, 1], c='r')
        plt.gca().invert_yaxis()

        pre_left = box_xy[..., 0] - box_wh[..., 0] / 2
        pre_top = box_xy[..., 1] - box_wh[..., 1] / 2

        rect1 = plt.Rectangle([pre_left[0, 5, 5, 0], pre_top[0, 5, 5, 0]], box_wh[0, 5, 5, 0, 0], box_wh[0, 5, 5, 0, 1],
                              color="r", fill=False)
        rect2 = plt.Rectangle([pre_left[0, 5, 5, 1], pre_top[0, 5, 5, 1]], box_wh[0, 5, 5, 1, 0], box_wh[0, 5, 5, 1, 1],
                              color="r", fill=False)
        rect3 = plt.Rectangle([pre_left[0, 5, 5, 2], pre_top[0, 5, 5, 2]], box_wh[0, 5, 5, 2, 0], box_wh[0, 5, 5, 2, 1],
                              color="r", fill=False)

        ax.add_patch(rect1)
        ax.add_patch(rect2)
        ax.add_patch(rect3)

        plt.show()
        #


    feat = np.random.normal(0, 0.5, [4, 13, 13, 75])
    anchors = [[142, 110], [192, 243], [459, 401]]
    get_anchors_and_decode(feat, anchors, 20)

# -------------------------------------------------#
#   一共七个大结构块，每个大结构块都有特定的参数
# -------------------------------------------------#
DEFAULT_BLOCKS_ARGS = [
    {'kernel_size': 3, 'repeats': 1, 'filters_in': 32, 'filters_out': 16,
     'expand_ratio': 1, 'id_skip': True, 'strides': 1, 'se_ratio': 0.25},

    {'kernel_size': 3, 'repeats': 2, 'filters_in': 16, 'filters_out': 24,
     'expand_ratio': 6, 'id_skip': True, 'strides': 2, 'se_ratio': 0.25},

    {'kernel_size': 5, 'repeats': 2, 'filters_in': 24, 'filters_out': 40,
     'expand_ratio': 6, 'id_skip': True, 'strides': 2, 'se_ratio': 0.25},

    {'kernel_size': 3, 'repeats': 3, 'filters_in': 40, 'filters_out': 80,
     'expand_ratio': 6, 'id_skip': True, 'strides': 2, 'se_ratio': 0.25},

    {'kernel_size': 5, 'repeats': 3, 'filters_in': 80, 'filters_out': 112,
     'expand_ratio': 6, 'id_skip': True, 'strides': 1, 'se_ratio': 0.25},

    {'kernel_size': 5, 'repeats': 4, 'filters_in': 112, 'filters_out': 192,
     'expand_ratio': 6, 'id_skip': True, 'strides': 2, 'se_ratio': 0.25},

    {'kernel_size': 3, 'repeats': 1, 'filters_in': 192, 'filters_out': 320,
     'expand_ratio': 6, 'id_skip': True, 'strides': 1, 'se_ratio': 0.25}
]

# -------------------------------------------------#
#   Kernel的初始化器
# -------------------------------------------------#
CONV_KERNEL_INITIALIZER = {
    'class_name': 'VarianceScaling',
    'config': {
        'scale': 2.0,
        'mode': 'fan_out',
        'distribution': 'normal'
    }
}


# -------------------------------------------------#
#   用于计算卷积层的padding的大小
# -------------------------------------------------#
def correct_pad(inputs, kernel_size):
    img_dim = 1
    input_size = backend.int_shape(inputs)[img_dim:(img_dim + 2)]

    if isinstance(kernel_size, int):
        kernel_size = (kernel_size, kernel_size)

    if input_size[0] is None:
        adjust = (1, 1)
    else:
        adjust = (1 - input_size[0] % 2, 1 - input_size[1] % 2)

    correct = (kernel_size[0] // 2, kernel_size[1] // 2)

    return ((correct[0] - adjust[0], correct[0]),
            (correct[1] - adjust[1], correct[1]))


# -------------------------------------------------#
#   该函数的目的是保证filter的大小可以被8整除
# -------------------------------------------------#
def round_filters(filters, divisor, width_coefficient):
    filters *= width_coefficient
    new_filters = max(divisor, int(filters + divisor / 2) // divisor * divisor)
    if new_filters < 0.9 * filters:
        new_filters += divisor
    return int(new_filters)


# -------------------------------------------------#
#   计算模块的重复次数
# -------------------------------------------------#
def round_repeats(repeats, depth_coefficient):
    return int(math.ceil(depth_coefficient * repeats))


# -------------------------------------------------#
#   efficient_block
# -------------------------------------------------#
def block(inputs, activation_fn=tf.nn.swish, drop_rate=0., name='',
          filters_in=32, filters_out=16, kernel_size=3, strides=1,
          expand_ratio=1, se_ratio=0., id_skip=True):
    filters = filters_in * expand_ratio
    # -------------------------------------------------#
    #   利用Inverted residuals
    #   part1 利用1x1卷积进行通道数上升
    # -------------------------------------------------#
    if expand_ratio != 1:
        x = layers.Conv2D(filters, 1,
                          padding='same',
                          use_bias=False,
                          kernel_initializer=CONV_KERNEL_INITIALIZER,
                          name=name + 'expand_conv')(inputs)
        x = layers.BatchNormalization(axis=3, name=name + 'expand_bn')(x)
        x = layers.Activation(activation_fn, name=name + 'expand_activation')(x)
    else:
        x = inputs

    # ------------------------------------------------------#
    #   如果步长为2x2的话，利用深度可分离卷积进行高宽压缩
    #   part2 利用3x3卷积对每一个channel进行卷积
    # ------------------------------------------------------#
    if strides == 2:
        x = layers.ZeroPadding2D(padding=correct_pad(x, kernel_size),
                                 name=name + 'dwconv_pad')(x)
        conv_pad = 'valid'
    else:
        conv_pad = 'same'

    x = layers.DepthwiseConv2D(kernel_size,
                               strides=strides,
                               padding=conv_pad,
                               use_bias=False,
                               depthwise_initializer=CONV_KERNEL_INITIALIZER,
                               name=name + 'dwconv')(x)
    x = layers.BatchNormalization(axis=3, name=name + 'bn')(x)
    x = layers.Activation(activation_fn, name=name + 'activation')(x)

    # ------------------------------------------------------#
    #   完成深度可分离卷积后
    #   对深度可分离卷积的结果施加注意力机制
    # ------------------------------------------------------#
    if 0 < se_ratio <= 1:
        filters_se = max(1, int(filters_in * se_ratio))
        se = layers.GlobalAveragePooling2D(name=name + 'se_squeeze')(x)
        se = layers.Reshape((1, 1, filters), name=name + 'se_reshape')(se)
        # ------------------------------------------------------#
        #   通道先压缩后上升，最后利用sigmoid将值固定到0-1之间
        # ------------------------------------------------------#
        se = layers.Conv2D(filters_se, 1,
                           padding='same',
                           activation=activation_fn,
                           kernel_initializer=CONV_KERNEL_INITIALIZER,
                           name=name + 'se_reduce')(se)
        se = layers.Conv2D(filters, 1,
                           padding='same',
                           activation='sigmoid',
                           kernel_initializer=CONV_KERNEL_INITIALIZER,
                           name=name + 'se_expand')(se)
        x = layers.multiply([x, se], name=name + 'se_excite')

    # ------------------------------------------------------#
    #   part3 利用1x1卷积进行通道下降
    # ------------------------------------------------------#
    x = layers.Conv2D(filters_out, 1,
                      padding='same',
                      use_bias=False,
                      kernel_initializer=CONV_KERNEL_INITIALIZER,
                      name=name + 'project_conv')(x)
    x = layers.BatchNormalization(axis=3, name=name + 'project_bn')(x)

    # ------------------------------------------------------#
    #   part4 如果满足残差条件，那么就增加残差边
    # ------------------------------------------------------#
    if (id_skip is True and strides == 1 and filters_in == filters_out):
        if drop_rate > 0:
            x = layers.Dropout(drop_rate,
                               noise_shape=(None, 1, 1, 1),
                               name=name + 'drop')(x)
        x = layers.add([x, inputs], name=name + 'add')

    return x


def EfficientNet(width_coefficient,
                 depth_coefficient,
                 drop_connect_rate=0.2,
                 depth_divisor=8,
                 activation_fn=tf.nn.swish,
                 blocks_args=DEFAULT_BLOCKS_ARGS,
                 inputs=None,
                 **kwargs):
    img_input = inputs

    # -------------------------------------------------#
    #   创建stem部分
    #   416,416,3 -> 208,208,32
    # -------------------------------------------------#
    x = img_input
    x = layers.ZeroPadding2D(padding=correct_pad(x, 3),
                             name='stem_conv_pad')(x)
    x = layers.Conv2D(round_filters(32, depth_divisor, width_coefficient), 3,
                      strides=2,
                      padding='valid',
                      use_bias=False,
                      kernel_initializer=CONV_KERNEL_INITIALIZER,
                      name='stem_conv')(x)
    x = layers.BatchNormalization(axis=3, name='stem_bn')(x)
    x = layers.Activation(activation_fn, name='stem_activation')(x)

    # -------------------------------------------------#
    #   进行一个深度的copy
    # -------------------------------------------------#
    blocks_args = deepcopy(blocks_args)

    # -------------------------------------------------#
    #   计算总的efficient_block的数量
    # -------------------------------------------------#
    b = 0
    blocks = float(sum(args['repeats'] for args in blocks_args))

    feats = []
    filters_outs = []
    # ------------------------------------------------------------------------------#
    #   对结构块参数进行循环、一共进行7个大的结构块。
    #   每个大结构块下会重复小的efficient_block、每个大结构块的shape变化为：
    #   208,208,32 -> 208,208,16 -> 104,104,24 -> 52,52,40
    #   -> 26,26,80 -> 26,26,112 -> 13,13,192 -> 13,13,320
    #   输入为208,208,32，最终获得三个shape的有效特征层
    #   104,104,24、26,26,112、13,13,320
    # ------------------------------------------------------------------------------#
    for (i, args) in enumerate(blocks_args):
        assert args['repeats'] > 0
        args['filters_in'] = round_filters(args['filters_in'], depth_divisor, width_coefficient)
        args['filters_out'] = round_filters(args['filters_out'], depth_divisor, width_coefficient)

        for j in range(round_repeats(args.pop('repeats'), depth_coefficient)):
            if j > 0:
                args['strides'] = 1
                args['filters_in'] = args['filters_out']
            x = block(x, activation_fn, drop_connect_rate * b / blocks,
                      name='block{}{}_'.format(i + 1, chr(j + 97)), **args)
            b += 1
        feats.append(x)
        if i == 2 or i == 4 or i == 6:
            filters_outs.append(args['filters_out'])
    return feats, filters_outs


def EfficientNetB0(inputs=None, **kwargs):
    return EfficientNet(1.0, 1.0, inputs=inputs, **kwargs)


def EfficientNetB1(inputs=None, **kwargs):
    return EfficientNet(1.0, 1.1, inputs=inputs, **kwargs)


def EfficientNetB2(inputs=None, **kwargs):
    return EfficientNet(1.1, 1.2, inputs=inputs, **kwargs)


def EfficientNetB3(inputs=None, **kwargs):
    return EfficientNet(1.2, 1.4, inputs=inputs, **kwargs)


def EfficientNetB4(inputs=None, **kwargs):
    return EfficientNet(1.4, 1.8, inputs=inputs, **kwargs)


def EfficientNetB5(inputs=None, **kwargs):
    return EfficientNet(1.6, 2.2, inputs=inputs, **kwargs)


def EfficientNetB6(inputs=None, **kwargs):
    return EfficientNet(1.8, 2.6, inputs=inputs, **kwargs)


def EfficientNetB7(inputs=None, **kwargs):
    return EfficientNet(2.0, 3.1, inputs=inputs, **kwargs)


if __name__ == '__main__':
    print(EfficientNetB0())


def box_ciou(b1, b2):
    """
    输入为：
    ----------
    b1: tensor, shape=(batch, feat_w, feat_h, anchor_num, 4), xywh
    b2: tensor, shape=(batch, feat_w, feat_h, anchor_num, 4), xywh

    返回为：
    -------
    ciou: tensor, shape=(batch, feat_w, feat_h, anchor_num, 1)
    """
    # -----------------------------------------------------------#
    #   求出预测框左上角右下角
    #   b1_mins     (batch, feat_w, feat_h, anchor_num, 2)
    #   b1_maxes    (batch, feat_w, feat_h, anchor_num, 2)
    # -----------------------------------------------------------#
    b1_xy = b1[..., :2]
    b1_wh = b1[..., 2:4]
    b1_wh_half = b1_wh / 2.
    b1_mins = b1_xy - b1_wh_half
    b1_maxes = b1_xy + b1_wh_half
    # -----------------------------------------------------------#
    #   求出真实框左上角右下角
    #   b2_mins     (batch, feat_w, feat_h, anchor_num, 2)
    #   b2_maxes    (batch, feat_w, feat_h, anchor_num, 2)
    # -----------------------------------------------------------#
    b2_xy = b2[..., :2]
    b2_wh = b2[..., 2:4]
    b2_wh_half = b2_wh / 2.
    b2_mins = b2_xy - b2_wh_half
    b2_maxes = b2_xy + b2_wh_half

    # -----------------------------------------------------------#
    #   求真实框和预测框所有的iou
    #   iou         (batch, feat_w, feat_h, anchor_num)
    # -----------------------------------------------------------#
    intersect_mins = K.maximum(b1_mins, b2_mins)
    intersect_maxes = K.minimum(b1_maxes, b2_maxes)
    intersect_wh = K.maximum(intersect_maxes - intersect_mins, 0.)
    intersect_area = intersect_wh[..., 0] * intersect_wh[..., 1]
    b1_area = b1_wh[..., 0] * b1_wh[..., 1]
    b2_area = b2_wh[..., 0] * b2_wh[..., 1]
    union_area = b1_area + b2_area - intersect_area
    iou = intersect_area / K.maximum(union_area, K.epsilon())

    # -----------------------------------------------------------#
    #   计算中心的差距
    #   center_distance (batch, feat_w, feat_h, anchor_num)
    # -----------------------------------------------------------#
    center_distance = K.sum(K.square(b1_xy - b2_xy), axis=-1)
    enclose_mins = K.minimum(b1_mins, b2_mins)
    enclose_maxes = K.maximum(b1_maxes, b2_maxes)
    enclose_wh = K.maximum(enclose_maxes - enclose_mins, 0.0)
    # -----------------------------------------------------------#
    #   计算对角线距离
    #   enclose_diagonal (batch, feat_w, feat_h, anchor_num)
    # -----------------------------------------------------------#
    enclose_diagonal = K.sum(K.square(enclose_wh), axis=-1)
    ciou = iou - 1.0 * (center_distance) / K.maximum(enclose_diagonal, K.epsilon())

    v = 4 * K.square(tf.math.atan2(b1_wh[..., 0], K.maximum(b1_wh[..., 1], K.epsilon())) - tf.math.atan2(b2_wh[..., 0],
                                                                                                         K.maximum(
                                                                                                             b2_wh[
                                                                                                                 ..., 1],
                                                                                                             K.epsilon()))) / (
                    math.pi * math.pi)
    alpha = v / K.maximum((1.0 - iou + v), K.epsilon())
    ciou = ciou - alpha * v

    ciou = K.expand_dims(ciou, -1)
    return ciou


# ---------------------------------------------------#
#   用于计算每个预测框与真实框的iou
# ---------------------------------------------------#
def box_iou(b1, b2):
    # ---------------------------------------------------#
    #   num_anchor,1,4
    #   计算左上角的坐标和右下角的坐标
    # ---------------------------------------------------#
    b1 = K.expand_dims(b1, -2)
    b1_xy = b1[..., :2]
    b1_wh = b1[..., 2:4]
    b1_wh_half = b1_wh / 2.
    b1_mins = b1_xy - b1_wh_half
    b1_maxes = b1_xy + b1_wh_half

    # ---------------------------------------------------#
    #   1,n,4
    #   计算左上角和右下角的坐标
    # ---------------------------------------------------#
    b2 = K.expand_dims(b2, 0)
    b2_xy = b2[..., :2]
    b2_wh = b2[..., 2:4]
    b2_wh_half = b2_wh / 2.
    b2_mins = b2_xy - b2_wh_half
    b2_maxes = b2_xy + b2_wh_half

    # ---------------------------------------------------#
    #   计算重合面积
    # ---------------------------------------------------#
    intersect_mins = K.maximum(b1_mins, b2_mins)
    intersect_maxes = K.minimum(b1_maxes, b2_maxes)
    intersect_wh = K.maximum(intersect_maxes - intersect_mins, 0.)
    intersect_area = intersect_wh[..., 0] * intersect_wh[..., 1]
    b1_area = b1_wh[..., 0] * b1_wh[..., 1]
    b2_area = b2_wh[..., 0] * b2_wh[..., 1]
    iou = intersect_area / (b1_area + b2_area - intersect_area)
    return iou

# ---------------------------------------------------#
#   loss值计算
# ---------------------------------------------------#
def yolo_loss(
        args,
        input_shape,
        anchors,
        anchors_mask,
        num_classes,
        ignore_thresh=0.5,
        balance=[0.4, 1.0, 4],
        box_ratio=0.05,
        obj_ratio=1,
        cls_ratio=0.5 / 4,
        ciou_flag=True,
        print_loss=False
):
    num_layers = len(anchors_mask)
    # ---------------------------------------------------------------------------------------------------#
    #   将预测结果和实际ground truth分开，args是[*model_body.output, *y_true]
    #   y_true是一个列表，包含三个特征层，shape分别为:
    #   (m,13,13,3,85)
    #   (m,26,26,3,85)
    #   (m,52,52,3,85)
    #   yolo_outputs是一个列表，包含三个特征层，shape分别为:
    #   (m,13,13,3,85)
    #   (m,26,26,3,85)
    #   (m,52,52,3,85)
    # ---------------------------------------------------------------------------------------------------#
    y_true = args[num_layers:]
    yolo_outputs = args[:num_layers]

    # -----------------------------------------------------------#
    #   得到input_shpae为416,416
    # -----------------------------------------------------------#
    input_shape = K.cast(input_shape, K.dtype(y_true[0]))
    # -----------------------------------------------------------#
    #   得到网格的shape为[13,13]; [26,26]; [52,52]
    # -----------------------------------------------------------#
    grid_shapes = [K.cast(K.shape(yolo_outputs[l])[1:3], K.dtype(y_true[0])) for l in range(num_layers)]

    # -----------------------------------------------------------#
    #   取出每一张图片
    #   m的值就是batch_size
    # -----------------------------------------------------------#
    m = K.shape(yolo_outputs[0])[0]

    loss = 0
    # ---------------------------------------------------------------------------------------------------#
    #   y_true是一个列表，包含三个特征层，shape分别为(m,13,13,3,85),(m,26,26,3,85),(m,52,52,3,85)。
    #   yolo_outputs是一个列表，包含三个特征层，shape分别为(m,13,13,3,85),(m,26,26,3,85),(m,52,52,3,85)。
    # ---------------------------------------------------------------------------------------------------#
    for l in range(num_layers):
        # -----------------------------------------------------------#
        #   以第一个特征层(m,13,13,3,85)为例子
        #   取出该特征层中存在目标的点的位置。(m,13,13,3,1)
        # -----------------------------------------------------------#
        object_mask = y_true[l][..., 4:5]
        # -----------------------------------------------------------#
        #   取出其对应的种类(m,13,13,3,80)
        # -----------------------------------------------------------#
        true_class_probs = y_true[l][..., 5:]

        # -----------------------------------------------------------#
        #   将yolo_outputs的特征层输出进行处理、获得四个返回值
        #   其中：
        #   grid        (13,13,1,2) 网格坐标
        #   raw_pred    (m,13,13,3,85) 尚未处理的预测结果
        #   pred_xy     (m,13,13,3,2) 解码后的中心坐标
        #   pred_wh     (m,13,13,3,2) 解码后的宽高坐标
        # -----------------------------------------------------------#
        grid, raw_pred, pred_xy, pred_wh = get_anchors_and_decode(yolo_outputs[l],
                                                                  anchors[anchors_mask[l]], num_classes, input_shape,
                                                                  calc_loss=True)

        # -----------------------------------------------------------#
        #   pred_box是解码后的预测的box的位置
        #   (m,13,13,3,4)
        # -----------------------------------------------------------#
        pred_box = K.concatenate([pred_xy, pred_wh])

        # -----------------------------------------------------------#
        #   找到负样本群组，第一步是创建一个数组，[]
        # -----------------------------------------------------------#
        ignore_mask = tf.TensorArray(K.dtype(y_true[0]), size=1, dynamic_size=True)
        object_mask_bool = K.cast(object_mask, 'bool')

        # -----------------------------------------------------------#
        #   对每一张图片计算ignore_mask
        # -----------------------------------------------------------#
        def loop_body(b, ignore_mask):
            # -----------------------------------------------------------#
            #   取出n个真实框：n,4
            # -----------------------------------------------------------#
            true_box = tf.boolean_mask(y_true[l][b, ..., 0:4], object_mask_bool[b, ..., 0])
            # -----------------------------------------------------------#
            #   计算预测框与真实框的iou
            #   pred_box    13,13,3,4 预测框的坐标
            #   true_box    n,4 真实框的坐标
            #   iou         13,13,3,n 预测框和真实框的iou
            # -----------------------------------------------------------#
            iou = box_iou(pred_box[b], true_box)

            # -----------------------------------------------------------#
            #   best_iou    13,13,3 每个特征点与真实框的最大重合程度
            # -----------------------------------------------------------#
            best_iou = K.max(iou, axis=-1)

            # -----------------------------------------------------------#
            #   判断预测框和真实框的最大iou小于ignore_thresh
            #   则认为该预测框没有与之对应的真实框
            #   该操作的目的是：
            #   忽略预测结果与真实框非常对应特征点，因为这些框已经比较准了
            #   不适合当作负样本，所以忽略掉。
            # -----------------------------------------------------------#
            ignore_mask = ignore_mask.write(b, K.cast(best_iou < ignore_thresh, K.dtype(true_box)))
            return b + 1, ignore_mask

        # -----------------------------------------------------------#
        #   在这个地方进行一个循环、循环是对每一张图片进行的
        # -----------------------------------------------------------#
        _, ignore_mask = tf.while_loop(lambda b, *args: b < m, loop_body, [0, ignore_mask])

        # -----------------------------------------------------------#
        #   ignore_mask用于提取出作为负样本的特征点
        #   (m,13,13,3)
        # -----------------------------------------------------------#
        ignore_mask = ignore_mask.stack()
        #   (m,13,13,3,1)
        ignore_mask = K.expand_dims(ignore_mask, -1)

        # -----------------------------------------------------------#
        #   reshape_y_true[...,2:3]和reshape_y_true[...,3:4]
        #   表示真实框的宽高，二者均在0-1之间
        #   真实框越大，比重越小，小框的比重更大。
        # -----------------------------------------------------------#
        box_loss_scale = 2 - y_true[l][..., 2:3] * y_true[l][..., 3:4]
        if ciou_flag:
            # -----------------------------------------------------------#
            #   计算Ciou loss
            # -----------------------------------------------------------#
            raw_true_box = y_true[l][..., 0:4]
            ciou = box_ciou(pred_box, raw_true_box)
            ciou_loss = object_mask * (1 - ciou)
            location_loss = K.sum(ciou_loss)
        else:
            # -----------------------------------------------------------#
            #   将真实框进行编码，使其格式与预测的相同，后面用于计算loss
            # -----------------------------------------------------------#
            raw_true_xy = y_true[l][..., :2] * grid_shapes[l][::-1] - grid
            raw_true_wh = K.log(y_true[l][..., 2:4] / anchors[anchors_mask[l]] * input_shape[::-1])

            # -----------------------------------------------------------#
            #   object_mask如果真实存在目标则保存其wh值
            #   switch接口，就是一个if/else条件判断语句
            # -----------------------------------------------------------#
            raw_true_wh = K.switch(object_mask, raw_true_wh, K.zeros_like(raw_true_wh))
            # -----------------------------------------------------------#
            #   利用binary_crossentropy计算中心点偏移情况，效果更好
            # -----------------------------------------------------------#
            xy_loss = object_mask * box_loss_scale * K.binary_crossentropy(raw_true_xy, raw_pred[..., 0:2],
                                                                           from_logits=True)
            # -----------------------------------------------------------#
            #   wh_loss用于计算宽高损失
            # -----------------------------------------------------------#
            wh_loss = object_mask * box_loss_scale * 0.5 * K.square(raw_true_wh - raw_pred[..., 2:4])
            location_loss = (K.sum(xy_loss) + K.sum(wh_loss)) * 0.1

        # ------------------------------------------------------------------------------#
        #   如果该位置本来有框，那么计算1与置信度的交叉熵
        #   如果该位置本来没有框，那么计算0与置信度的交叉熵
        #   在这其中会忽略一部分样本，这些被忽略的样本满足条件best_iou<ignore_thresh
        #   该操作的目的是：
        #   忽略预测结果与真实框非常对应特征点，因为这些框已经比较准了
        #   不适合当作负样本，所以忽略掉。
        # ------------------------------------------------------------------------------#
        confidence_loss = object_mask * K.binary_crossentropy(object_mask, raw_pred[..., 4:5], from_logits=True) + \
                          (1 - object_mask) * K.binary_crossentropy(object_mask, raw_pred[..., 4:5],
                                                                    from_logits=True) * ignore_mask

        class_loss = object_mask * K.binary_crossentropy(true_class_probs, raw_pred[..., 5:], from_logits=True)

        # -----------------------------------------------------------#
        #   计算正样本数量
        # -----------------------------------------------------------#
        num_pos = tf.maximum(K.sum(K.cast(object_mask, tf.float32)), 1)
        num_neg = tf.maximum(K.sum(K.cast((1 - object_mask) * ignore_mask, tf.float32)), 1)
        # -----------------------------------------------------------#
        #   将所有损失求和
        # -----------------------------------------------------------#
        location_loss = location_loss * box_ratio / num_pos
        confidence_loss = K.sum(confidence_loss) * balance[l] * obj_ratio / (num_pos + num_neg)
        class_loss = K.sum(class_loss) * cls_ratio / num_pos / num_classes

        loss += location_loss + confidence_loss + class_loss
        if print_loss:
            loss = tf.Print(loss, [loss, location_loss, confidence_loss, class_loss, tf.shape(ignore_mask)],
                            summarize=100, message='loss: ')
    return loss


def get_lr_scheduler(lr_decay_type, lr, min_lr, total_iters, warmup_iters_ratio=0.05, warmup_lr_ratio=0.1,
                     no_aug_iter_ratio=0.05, step_num=10):
    def yolox_warm_cos_lr(lr, min_lr, total_iters, warmup_total_iters, warmup_lr_start, no_aug_iter, iters):
        if iters <= warmup_total_iters:
            # lr = (lr - warmup_lr_start) * iters / float(warmup_total_iters) + warmup_lr_start
            lr = (lr - warmup_lr_start) * pow(iters / float(warmup_total_iters), 2
                                              ) + warmup_lr_start
        elif iters >= total_iters - no_aug_iter:
            lr = min_lr
        else:
            lr = min_lr + 0.5 * (lr - min_lr) * (
                    1.0
                    + math.cos(
                math.pi
                * (iters - warmup_total_iters)
                / (total_iters - warmup_total_iters - no_aug_iter)
            )
            )
        return lr

    def step_lr(lr, decay_rate, step_size, iters):
        if step_size < 1:
            raise ValueError("step_size must above 1.")
        n = iters // step_size
        out_lr = lr * decay_rate ** n
        return out_lr

    if lr_decay_type == "cos":
        warmup_total_iters = min(max(warmup_iters_ratio * total_iters, 1), 3)
        warmup_lr_start = max(warmup_lr_ratio * lr, 1e-6)
        no_aug_iter = min(max(no_aug_iter_ratio * total_iters, 1), 15)
        func = partial(yolox_warm_cos_lr, lr, min_lr, total_iters, warmup_total_iters, warmup_lr_start, no_aug_iter)
    else:
        decay_rate = (min_lr / lr) ** (1 / (step_num - 1))
        step_size = total_iters / step_num
        func = partial(step_lr, lr, decay_rate, step_size)

    return func

###########################


Efficient = [EfficientNetB0,EfficientNetB1,EfficientNetB2,EfficientNetB3,EfficientNetB4,EfficientNetB5,EfficientNetB6,EfficientNetB7]

#------------------------------------------------------#
#   单次卷积
#   DarknetConv2D
#------------------------------------------------------#
@wraps(Conv2D)
def DarknetConv2D(*args, **kwargs):
    darknet_conv_kwargs = {'kernel_initializer' : RandomNormal(stddev=0.02), 'kernel_regularizer' : l2(kwargs.get('weight_decay', 5e-4))}
    darknet_conv_kwargs['padding'] = 'valid' if kwargs.get('strides')==(2, 2) else 'same'   
    try:
        del kwargs['weight_decay']
    except:
        pass
    darknet_conv_kwargs.update(kwargs)
    return Conv2D(*args, **darknet_conv_kwargs)
    
#---------------------------------------------------#
#   卷积块 -> 卷积 + 标准化 + 激活函数
#   DarknetConv2D + BatchNormalization + LeakyReLU
#---------------------------------------------------#
def DarknetConv2D_BN_Leaky(*args, **kwargs):
    no_bias_kwargs = {'use_bias': False}
    no_bias_kwargs.update(kwargs)
    return compose( 
        DarknetConv2D(*args, **no_bias_kwargs),
        BatchNormalization(),
        LeakyReLU(alpha=0.1))

#---------------------------------------------------#
#   特征层->最后的输出
#---------------------------------------------------#
def make_five_conv(x, num_filters, weight_decay=5e-4):
    x = DarknetConv2D_BN_Leaky(num_filters, (1,1), weight_decay=weight_decay)(x)
    x = DarknetConv2D_BN_Leaky(num_filters*2, (3,3), weight_decay=weight_decay)(x)
    x = DarknetConv2D_BN_Leaky(num_filters, (1,1), weight_decay=weight_decay)(x)
    x = DarknetConv2D_BN_Leaky(num_filters*2, (3,3), weight_decay=weight_decay)(x)
    x = DarknetConv2D_BN_Leaky(num_filters, (1,1), weight_decay=weight_decay)(x)
    return x

def make_yolo_head(x, num_filters, out_filters, weight_decay=5e-4):
    y = DarknetConv2D_BN_Leaky(num_filters*2, (3,3), weight_decay=weight_decay)(x)
    y = DarknetConv2D(out_filters, (1,1), weight_decay=weight_decay)(y)
    return y

#---------------------------------------------------#
#   FPN网络的构建，并且获得预测结果
#---------------------------------------------------#
def yolo_body(input_shape, anchors_mask, num_classes, phi = 0, weight_decay=5e-4):
    inputs      = Input(input_shape)
    #---------------------------------------------------#   
    #   生成efficientnet的主干模型，以efficientnetB0为例
    #   获得三个有效特征层，他们的shape分别是：
    #   52, 52, 40
    #   26, 26, 112
    #   13, 13, 320
    #---------------------------------------------------#
    feats, filters_outs = Efficient[phi](inputs = inputs)
    feat1 = feats[2]
    feat2 = feats[4]
    feat3 = feats[6]

    #------------------------------------------------------------------------#
    #   以efficientnet网络的输出通道数，构建FPN
    #------------------------------------------------------------------------#

    x   = make_five_conv(feat3, int(filters_outs[2]), weight_decay)
    #---------------------------------------------------#
    #   第一个特征层
    #   out0 = (batch_size, 255, 13, 13)
    #---------------------------------------------------#
    P5  = make_yolo_head(x, int(filters_outs[2]), len(anchors_mask[0]) * (num_classes+5), weight_decay)

    x   = compose(DarknetConv2D_BN_Leaky(int(filters_outs[1]), (1,1), weight_decay=weight_decay), UpSampling2D(2))(x)

    x   = Concatenate()([x, feat2])
    x   = make_five_conv(x, int(filters_outs[1]), weight_decay)
    #---------------------------------------------------#
    #   第二个特征层
    #   out1 = (batch_size, 255, 26, 26)
    #---------------------------------------------------#
    P4  = make_yolo_head(x, int(filters_outs[1]), len(anchors_mask[1]) * (num_classes+5), weight_decay)

    x   = compose(DarknetConv2D_BN_Leaky(int(filters_outs[0]), (1,1), weight_decay=weight_decay), UpSampling2D(2))(x)

    x   = Concatenate()([x, feat1])
    x   = make_five_conv(x, int(filters_outs[0]), weight_decay)
    #---------------------------------------------------#
    #   第三个特征层
    #   out3 = (batch_size, 255, 52, 52)
    #---------------------------------------------------#
    P3  = make_yolo_head(x, int(filters_outs[0]), len(anchors_mask[2]) * (num_classes+5), weight_decay)
    return Model(inputs, [P5, P4, P3])


def get_train_model(model_body, input_shape, num_classes, anchors, anchors_mask):
    y_true = [Input(shape = (input_shape[0] // {0:32, 1:16, 2:8}[l], input_shape[1] // {0:32, 1:16, 2:8}[l], \
                                len(anchors_mask[l]), num_classes + 5)) for l in range(len(anchors_mask))]
    model_loss  = Lambda(
        yolo_loss, 
        output_shape    = (1, ), 
        name            = 'yolo_loss', 
        arguments       = {
            'input_shape'       : input_shape, 
            'anchors'           : anchors, 
            'anchors_mask'      : anchors_mask, 
            'num_classes'       : num_classes, 
            'balance'           : [0.4, 1.0, 4],
            'box_ratio'         : 0.05,
            'obj_ratio'         : 5 * (input_shape[0] * input_shape[1]) / (416 ** 2), 
            'cls_ratio'         : 1 * (num_classes / 80)
        }
    )([*model_body.output, *y_true])
    model       = Model([model_body.input, *y_true], model_loss)
    return model
