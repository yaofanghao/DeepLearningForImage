# import numpy as np
# from keras.models import *
# from keras import layers
# from keras.layers import *
# from nets.vgg16 import VGG16
# from nets.mobilenet import relu6
# from tensorflow.python.keras.models import Model
#
#
#
#
# def identity_block(input_tensor, kernel_size, filters, stage, block):
#     filters1, filters2, filters3 = filters
#
#     conv_name_base = 'res' + str(stage) + block + '_branch'
#     bn_name_base = 'bn' + str(stage) + block + '_branch'
#
#     x = Conv2D(filters1, (1, 1), name=conv_name_base + '2a')(input_tensor)
#     x = BatchNormalization(name=bn_name_base + '2a')(x)
#     x = Activation('relu')(x)
#
#     x = Conv2D(filters2, kernel_size, padding='same', name=conv_name_base + '2b')(x)
#     x = BatchNormalization(name=bn_name_base + '2b')(x)
#     x = Activation('relu')(x)
#
#     x = Conv2D(filters3, (1, 1), name=conv_name_base + '2c')(x)
#     x = BatchNormalization(name=bn_name_base + '2c')(x)
#
#     x = add([x, input_tensor])
#     x = Activation('relu')(x)
#     return x
#
# def hard_sigmoid(x):
#     return layers.ReLU(6.)(x+3)*(1./6.)
#
# def hard_swish(x):
#     return layers.Multiply()([hard_sigmoid(x),x])
#
#
# def squeeze(inputs):
#     input_channels = int(inputs.shape[-1])
#     x = GlobalAveragePooling2D()(inputs)
#     x = Dense(int(input_channels / 4))(x)
#     x = Activation(relu6)(x)
#     x = Dense(input_channels)(x)
#     x = Activation(hard_swish)(x)
#     x = Reshape((1, 1, input_channels))(x)
#     x = Multiply()([inputs, x])
#     return x
#
# def Unet(input_shape, num_classes):
#     inputs = Input(input_shape)
#     feat1, feat2, feat3, feat4, feat5 = VGG16(inputs)
#
#     channels = [64, 128, 256, 512]
#
#     P5_up = UpSampling2D(size=(2, 2))(feat5)
#     P4 = Concatenate(axis=3)([feat4, P5_up])
#     # P4 = identity_block(P4, 3, [512, 512, 1024], stage=4, block='a')
#     # P4 =squeeze(P4)
#     P4 = Conv2D(channels[3], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P4)
#     P4 = Conv2D(channels[3], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P4)
#
#     P4_up = UpSampling2D(size=(2, 2))(P4)
#     P3 = Concatenate(axis=3)([feat3, P4_up])
#     # P3 = identity_block(P3, 3, [512, 512, 768], stage=4, block='b')
#     # P3 = squeeze(P3)
#     P3 = Conv2D(channels[2], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P3)
#     P3 = Conv2D(channels[2], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P3)
#
#     P3_up = UpSampling2D(size=(2, 2))(P3)
#     P2 = Concatenate(axis=3)([feat2, P3_up])
#     # P2 = identity_block(P2, 3, [256, 256, 384], stage=4, block='c')
#     # P2 = squeeze(P2)
#     P2 = Conv2D(channels[1], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P2)
#     P2 = Conv2D(channels[1], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P2)
#
#     P2_up = UpSampling2D(size=(2, 2))(P2)
#     P1 = Concatenate(axis=3)([feat1, P2_up])
#     # P1 = identity_block(P1, 3, [128, 128, 192], stage=4, block='d')
#     # P1 = squeeze(P1)
#     P1 = Conv2D(channels[0], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P1)
#     P1 = Conv2D(channels[0], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P1)
#
#     P1 = Conv2D(num_classes, 1, activation="softmax")(P1)
#
#     model = Model(inputs=inputs, outputs=P1)
#     return model



from tensorflow.python.keras import layers
from tensorflow.python.keras.layers import *
from tensorflow.python.keras.models import Model
from nets.vgg16 import VGG16
# from tensorflow.python.keras.applications.mobilenet_v3 import hard_swish

from nets.mobilenet import relu6


def hard_sigmoid(x):
    return layers.ReLU(6.)(x+3)*(1./6.)

def hard_swish(x):
    return layers.Multiply()([hard_sigmoid(x),x])

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

    x = add([x, input_tensor])
    x = Activation('relu')(x)
    return x


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

def Unet(input_shape, num_classes):
    inputs = Input(input_shape)
    C1, C2, C3, C4, C5 = VGG16(inputs)

    channels = [64,128, 256,512]

    P5_up = UpSampling2D(size=(2, 2))(C5)
    P4 = Concatenate(axis=3)([C4, P5_up])
    # P4 = identity_block(P4, 3, [512, 512, 1024], stage=4, block='a')
    # P4 =squeeze(P4)
    P4 = Conv2D(channels[3], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P4)
    P4 = Conv2D(channels[3], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P4)

    P4_up = UpSampling2D(size=(2, 2))(P4)
    P3 = Concatenate(axis=3)([C3, P4_up])
    # P3 = identity_block(P3, 3, [512, 512, 768], stage=4, block='b')
    # P3 = squeeze(P3)
    P3 = Conv2D(channels[2], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P3)
    P3 = Conv2D(channels[2], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P3)

    P3_up = UpSampling2D(size=(2, 2))(P3)
    P2 = Concatenate(axis=3)([C2, P3_up])
    # P2 = identity_block(P2, 3, [256, 256, 384], stage=4, block='c')
    # P2 = squeeze(P2)
    P2 = Conv2D(channels[1], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P2)
    P2 = Conv2D(channels[1], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P2)

    P2_up = UpSampling2D(size=(2, 2))(P2)
    P1 = Concatenate(axis=3)([C1, P2_up])
    # P1 = identity_block(P1, 3, [128, 128, 192], stage=4, block='d')
    # P1 = squeeze(P1)
    P1 = Conv2D(channels[0], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P1)
    P1 = Conv2D(channels[0], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P1)

    P1 = Conv2D(num_classes, 1, activation="softmax")(P1)

    model = Model(inputs=inputs, outputs=P1)
    return model
