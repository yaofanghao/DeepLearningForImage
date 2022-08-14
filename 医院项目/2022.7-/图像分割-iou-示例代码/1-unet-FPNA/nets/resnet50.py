import keras
import keras.backend as K
from keras import layers
from keras.layers import *
from tensorflow.python.keras.applications.mobilenet_v3 import hard_swish

from nets.mobilenet import relu6


def squeeze(inputs):
    input_channels = int(inputs.shape[-1])

    x = GlobalAveragePooling2D()(inputs)
    x = Dense(int(input_channels / 4))(x)
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

    x = Conv2D(filters1, (1, 1), name=conv_name_base + '2a')(input_tensor)
    x = BatchNormalization(name=bn_name_base + '2a')(x)
    x = Activation('relu')(x)

    x = Conv2D(filters2, kernel_size, padding='same', name=conv_name_base + '2b')(x)
    x = BatchNormalization(name=bn_name_base + '2b')(x)
    x = Activation('relu')(x)

    x = Conv2D(filters3, (1, 1), name=conv_name_base + '2c')(x)
    x = BatchNormalization(name=bn_name_base + '2c')(x)

    x = layers.add([x, input_tensor])
    x = Activation('relu')(x)
    return x


def conv_block(input_tensor, kernel_size, filters, stage, block, strides=(2, 2)):
    filters1, filters2, filters3 = filters

    conv_name_base = 'res' + str(stage) + block + '_branch'
    bn_name_base = 'bn' + str(stage) + block + '_branch'

    x = Conv2D(filters1, (1, 1), strides=strides,
               name=conv_name_base + '2a')(input_tensor)
    x = BatchNormalization(name=bn_name_base + '2a')(x)
    x = Activation('relu')(x)

    x = Conv2D(filters2, kernel_size, padding='same',
               name=conv_name_base + '2b')(x)
    x = BatchNormalization(name=bn_name_base + '2b')(x)
    x = Activation('relu')(x)

    x = Conv2D(filters3, (1, 1), name=conv_name_base + '2c')(x)

    x = BatchNormalization(name=bn_name_base + '2c')(x)

    shortcut = Conv2D(filters3, (1, 1), strides=strides,
                      name=conv_name_base + '1')(input_tensor)
    shortcut = BatchNormalization(name=bn_name_base + '1')(shortcut)

    x = layers.add([x, shortcut])
    x = Activation('relu')(x)
    return x


def get_resnet50_encoder(img_input):
    # img_input = Input([input_height, input_width, 3])

    # 416,416,3 -> 208,208,32
    x = ZeroPadding2D((3, 3))(img_input)
    x = Conv2D(32, (7, 7), strides=(2, 2), name='conv1')(x)
    x = BatchNormalization(name='bn_conv1')(x)
    x = squeeze(x)
    x = Activation('relu')(x)
    f1 = x

    # 208,208,32 -> 104,104,32 -> 104,104,64
    x = MaxPooling2D((3, 3), strides=(2, 2), padding="same")(x)

    x = conv_block(x, 3, [32, 32, 64], stage=2, block='a', strides=(1, 1))
    # x = identity_block(x, 3, [32, 32, 64], stage=2, block='b')
    x = squeeze(x)
    x = identity_block(x, 3, [32, 32, 64], stage=2, block='c')
    # f2是hw方向压缩两次的结果
    f2 = x

    # 104,104,64 -> 52,52,128
    x = conv_block(x, 3, [64, 64, 128], stage=3, block='a')
    x = squeeze(x)
    x = identity_block(x, 3, [64, 64, 128], stage=3, block='b')
    # x = identity_block(x, 3, [64, 64, 128], stage=3, block='c')
    # x = identity_block(x, 3, [64, 64, 128], stage=3, block='d')
    # f3是hw方向压缩三次的结果
    f3 = x

    # 52,52,128 -> 26,26,256
    x = conv_block(x, 3, [128, 128, 256], stage=4, block='a')
    x = squeeze(x)
    x = identity_block(x, 3, [128, 128, 256], stage=4, block='b')
    x = squeeze(x)
    x = identity_block(x, 3, [128, 128, 256], stage=4, block='c')
    # x = identity_block(x, 3, [128, 128, 256], stage=4, block='d')
    # x = identity_block(x, 3, [128, 128, 256], stage=4, block='e')
    # x = identity_block(x, 3, [128, 128, 256], stage=4, block='f')
    # f4是hw方向压缩四次的结果
    x = Dropout(0.5)(x)
    f4 = x

    # 26,26,256 -> 13,13,512
    x = conv_block(x, 3, [256, 256, 512], stage=5, block='a')
    x = squeeze(x)
    x = identity_block(x, 3, [256, 256, 512], stage=5, block='b')
    x = squeeze(x)
    x = identity_block(x, 3, [256, 256, 512], stage=5, block='c')
    # f5是hw方向压缩五次的结果
    x = Dropout(0.5)(x)
    f5 = x

    return f1, f2, f3, f4, f5
