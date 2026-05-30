#   ResNet50的网络设计 2022.12.14修改
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.initializers import RandomNormal
from tensorflow.keras.layers import (Activation, Add, AveragePooling2D,
                                     BatchNormalization, Conv2D, MaxPooling2D,
                                     TimeDistributed, ZeroPadding2D,
                                     Dense, GlobalAveragePooling2D, Multiply, Reshape)
from keras import backend as K
# from keras.layers import (Activation, Add, BatchNormalization, Conv2D, Dense,
#                           DepthwiseConv2D, GlobalAveragePooling2D, Input,
#                           Multiply, Reshape)

#   设置使用leaky-relu
leaky_flag = True
#   设置是否加入SE注意力模块
attention_flag =True

#   激活函数 relu6
def relu6(x):
    return K.relu(x, max_value=6)

#   激活函数 leaky-relu 2022.12.14修改
def leaky_relu(x):
    leak = 0.1
    # if x>0 
    #   y=x
    # else y=0.2x
    return  (0.5+leak)*x+(0.5-leak)*tf.abs(x) 

#   激活函数 hard_swish, 利用relu函数乘上x模拟sigmoid
def hard_swish(x):
    return x * K.relu(x + 3.0, max_value=6.0) / 6.0

#   用于判断使用哪个激活函数
# def return_activation(x, activation):
#     if activation == 'HS':
#         x = Activation(hard_swish)(x)
#     if activation == 'RE':
#         x = Activation(relu6)(x)
#     return x

#   卷积块
#   卷积 + 标准化 + 激活函数
# def conv_block(inputs, filters, kernel, strides, activation):
#     x = Conv2D(filters, kernel, padding='same', strides=strides)(inputs)
#     x = BatchNormalization()(x)
#     return return_activation(x, activation)

#---------------------------------------#
#   通道注意力机制单元
#   利用两次全连接算出每个通道的比重
#   可以连接在任意特征层后面
#---------------------------------------#
def squeeze(inputs):
    input_channels = int(inputs.shape[-1])
    x = GlobalAveragePooling2D()(inputs)

    x = Dense(int(input_channels/4))(x)
    x = Activation(relu6)(x)

    x = Dense(input_channels)(x)
    x = Activation(hard_swish)(x)

    x = Reshape((1, 1, input_channels))(x)
    x = Multiply()([inputs, x])
    return x

def identity_block(input_tensor, kernel_size, filters, stage, block):

    filters1, filters2, filters3 = filters

    conv_name_base = 'res' + str(stage) + block + '_branch'
    bn_name_base = 'bn' + str(stage) + block + '_branch'

    x = Conv2D(filters1, (1, 1), kernel_initializer=RandomNormal(stddev=0.02), name=conv_name_base + '2a')(input_tensor)
    x = BatchNormalization(trainable=False, name=bn_name_base + '2a')(x)
    if leaky_flag:
        x = leaky_relu(x) 
    else:
        x = Activation('relu')(x)

    x = Conv2D(filters2, kernel_size, padding='same', kernel_initializer=RandomNormal(stddev=0.02), name=conv_name_base + '2b')(x)
    x = BatchNormalization(trainable=False, name=bn_name_base + '2b')(x)
    if leaky_flag:
        x = leaky_relu(x) 
    else:
        x = Activation('relu')(x)

    x = Conv2D(filters3, (1, 1), kernel_initializer=RandomNormal(stddev=0.02), name=conv_name_base + '2c')(x)
    x = BatchNormalization(trainable=False, name=bn_name_base + '2c')(x)

    x = layers.add([x, input_tensor])
    if leaky_flag:
        x = leaky_relu(x) 
    else:
        x = Activation('relu')(x)
    return x

def conv_block(input_tensor, kernel_size, filters, stage, block, strides=(2, 2)):

    filters1, filters2, filters3 = filters

    conv_name_base = 'res' + str(stage) + block + '_branch'
    bn_name_base = 'bn' + str(stage) + block + '_branch'

    x = Conv2D(filters1, (1, 1), strides=strides, kernel_initializer=RandomNormal(stddev=0.02),
               name=conv_name_base + '2a')(input_tensor)
    x = BatchNormalization(trainable=False, name=bn_name_base + '2a')(x)
    if leaky_flag:
        x = leaky_relu(x) 
    else:
        x = Activation('relu')(x)

    x = Conv2D(filters2, kernel_size, padding='same', kernel_initializer=RandomNormal(stddev=0.02),
               name=conv_name_base + '2b')(x)
    x = BatchNormalization(trainable=False, name=bn_name_base + '2b')(x)
    if leaky_flag:
        x = leaky_relu(x) 
    else:
        x = Activation('relu')(x)

    x = Conv2D(filters3, (1, 1), kernel_initializer=RandomNormal(stddev=0.02), name=conv_name_base + '2c')(x)
    x = BatchNormalization(trainable=False, name=bn_name_base + '2c')(x)

    shortcut = Conv2D(filters3, (1, 1), strides=strides, kernel_initializer=RandomNormal(stddev=0.02),
                      name=conv_name_base + '1')(input_tensor)
    shortcut = BatchNormalization(trainable=False, name=bn_name_base + '1')(shortcut)

    x = layers.add([x, shortcut])
    if leaky_flag:
        x = leaky_relu(x) 
    else:
        x = Activation('relu')(x)
    return x

def ResNet50(inputs):
    #-----------------------------------#
    #   假设输入进来的图片是600,600,3
    #-----------------------------------#
    img_input = inputs

    # 600,600,3 -> 300,300,64
    x = ZeroPadding2D((3, 3))(img_input)
    x = Conv2D(64, (7, 7), strides=(2, 2), name='conv1')(x)
    x = BatchNormalization(trainable=False, name='bn_conv1')(x)
    if leaky_flag:
        x = leaky_relu(x) 
    else:
        x = Activation('relu')(x)

    # 300,300,64 -> 150,150,64
    x = MaxPooling2D((3, 3), strides=(2, 2), padding="same")(x)

    # 150,150,64 -> 150,150,256
    x = conv_block(x, 3, [64, 64, 256], stage=2, block='a', strides=(1, 1))
    x = identity_block(x, 3, [64, 64, 256], stage=2, block='b')
    x = identity_block(x, 3, [64, 64, 256], stage=2, block='c')

    # 150,150,256 -> 75,75,512
    x = conv_block(x, 3, [128, 128, 512], stage=3, block='a')
    x = identity_block(x, 3, [128, 128, 512], stage=3, block='b')
    x = identity_block(x, 3, [128, 128, 512], stage=3, block='c')
    x = identity_block(x, 3, [128, 128, 512], stage=3, block='d')

    # 75,75,512 -> 38,38,1024
    x = conv_block(x, 3, [256, 256, 1024], stage=4, block='a')
    x = identity_block(x, 3, [256, 256, 1024], stage=4, block='b')
    x = identity_block(x, 3, [256, 256, 1024], stage=4, block='c')
    x = identity_block(x, 3, [256, 256, 1024], stage=4, block='d')
    x = identity_block(x, 3, [256, 256, 1024], stage=4, block='e')
    x = identity_block(x, 3, [256, 256, 1024], stage=4, block='f')

    # 在resnet最后插入这个SE块
    if attention_flag:
        x = squeeze(x)
    else:
        pass

    # 最终获得一个38,38,1024的共享特征层
    return x

def identity_block_td(input_tensor, kernel_size, filters, stage, block):
    nb_filter1, nb_filter2, nb_filter3 = filters
    conv_name_base = 'res' + str(stage) + block + '_branch'
    bn_name_base = 'bn' + str(stage) + block + '_branch'

    x = TimeDistributed(Conv2D(nb_filter1, (1, 1), kernel_initializer='normal'), name=conv_name_base + '2a')(input_tensor)
    x = TimeDistributed(BatchNormalization(trainable=False), name=bn_name_base + '2a')(x)
    if leaky_flag:
        x = leaky_relu(x) 
    else:
        x = Activation('relu')(x)

    x = TimeDistributed(Conv2D(nb_filter2, (kernel_size, kernel_size), kernel_initializer='normal',padding='same'), name=conv_name_base + '2b')(x)
    x = TimeDistributed(BatchNormalization(trainable=False), name=bn_name_base + '2b')(x)
    if leaky_flag:
        x = leaky_relu(x) 
    else:
        x = Activation('relu')(x)

    x = TimeDistributed(Conv2D(nb_filter3, (1, 1), kernel_initializer='normal'), name=conv_name_base + '2c')(x)
    x = TimeDistributed(BatchNormalization(trainable=False), name=bn_name_base + '2c')(x)

    x = Add()([x, input_tensor])
    if leaky_flag:
        x = leaky_relu(x) 
    else:
        x = Activation('relu')(x)

    return x

def conv_block_td(input_tensor, kernel_size, filters, stage, block, strides=(2, 2)):
    nb_filter1, nb_filter2, nb_filter3 = filters
    conv_name_base = 'res' + str(stage) + block + '_branch'
    bn_name_base = 'bn' + str(stage) + block + '_branch'

    x = TimeDistributed(Conv2D(nb_filter1, (1, 1), strides=strides, kernel_initializer='normal'), name=conv_name_base + '2a')(input_tensor)
    x = TimeDistributed(BatchNormalization(trainable=False), name=bn_name_base + '2a')(x)
    if leaky_flag:
        x = leaky_relu(x) 
    else:
        x = Activation('relu')(x)

    x = TimeDistributed(Conv2D(nb_filter2, (kernel_size, kernel_size), padding='same', kernel_initializer='normal'), name=conv_name_base + '2b')(x)
    x = TimeDistributed(BatchNormalization(trainable=False), name=bn_name_base + '2b')(x)
    if leaky_flag:
        x = leaky_relu(x) 
    else:
        x = Activation('relu')(x)

    x = TimeDistributed(Conv2D(nb_filter3, (1, 1), kernel_initializer='normal'), name=conv_name_base + '2c')(x)
    x = TimeDistributed(BatchNormalization(trainable=False), name=bn_name_base + '2c')(x)

    shortcut = TimeDistributed(Conv2D(nb_filter3, (1, 1), strides=strides, kernel_initializer='normal'), name=conv_name_base + '1')(input_tensor)
    shortcut = TimeDistributed(BatchNormalization(trainable=False), name=bn_name_base + '1')(shortcut)

    x = Add()([x, shortcut])
    if leaky_flag:
        x = leaky_relu(x) 
    else:
        x = Activation('relu')(x)
    return x

def resnet50_classifier_layers(x):
    # batch_size, num_rois, 14, 14, 1024 -> batch_size, num_rois, 7, 7, 2048
    x = conv_block_td(x, 3, [512, 512, 2048], stage=5, block='a', strides=(2, 2))
    # batch_size, num_rois, 7, 7, 2048 -> batch_size, num_rois, 7, 7, 2048
    x = identity_block_td(x, 3, [512, 512, 2048], stage=5, block='b')
    # batch_size, num_rois, 7, 7, 2048 -> batch_size, num_rois, 7, 7, 2048
    x = identity_block_td(x, 3, [512, 512, 2048], stage=5, block='c')
    # batch_size, num_rois, 7, 7, 2048 -> batch_size, num_rois, 1, 1, 2048
    x = TimeDistributed(AveragePooling2D((7, 7)), name='avg_pool')(x)

    return x
