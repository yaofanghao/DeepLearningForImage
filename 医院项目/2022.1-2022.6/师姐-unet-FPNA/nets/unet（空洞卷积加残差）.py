import numpy as np
from keras import layers
from keras.models import *
from keras.layers import *
from nets.vgg16_KD import VGG16


def identity_block(input_tensor, kernel_size, filters, stage, block, dilation_rate=1):
    filters1, filters2, filters3 = filters

    conv_name_base = 'res' + str(stage) + block + '_branch'
    bn_name_base = 'bn' + str(stage) + block + '_branch'

    x = Conv2D(filters1, (1, 1), name=conv_name_base + '2a', use_bias=False)(input_tensor)
    x = BatchNormalization(name=bn_name_base + '2a')(x)
    x = Activation('relu')(x)

    x = Conv2D(filters2, kernel_size, padding='same', dilation_rate=dilation_rate, name=conv_name_base + '2b',
               use_bias=False)(x)
    x = BatchNormalization(name=bn_name_base + '2b')(x)
    x = Activation('relu')(x)

    x = Conv2D(filters3, (1, 1), name=conv_name_base + '2c', use_bias=False)(x)
    x = BatchNormalization(name=bn_name_base + '2c')(x)

    x = layers.add([x, input_tensor])
    x = Activation('relu')(x)
    return x


# --------------------------------------------------------------------
# def Unet(input_shape=(512,512,3), num_classes=21):
def Unet(input_shape, num_classes):
    inputs = Input(input_shape)
    feat1, feat2, feat3, feat4 = VGG16(inputs)

    channels = [64, 128, 256]

    # 64*64*512
    P4 = identity_block(feat4, 3, [256, 256, 512], stage=1, block='a')
    # 128 128 512
    P4_up = UpSampling2D(size=(2, 2))(P4)
    P3 = Concatenate(axis=3)([feat3, P4_up])
    # 128 128 256
    P3 = layers.Conv2D(channels[2], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P3)
    P3 = layers.Conv2D(channels[2], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P3)
    # 256 256 256
    P3_up = UpSampling2D(size=(2, 2))(P3)
    P2 = Concatenate(axis=3)([feat2, P3_up])
    # 256 256 128
    P2 = layers.Conv2D(channels[1], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P2)
    P2 = layers.Conv2D(channels[1], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P2)
    # 512,512,128
    P2_up = UpSampling2D(size=(2, 2))(P2)
    P1 = Concatenate(axis=3)([feat1, P2_up])
    P1 = layers.Conv2D(channels[0], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P1)
    P1 = layers.Conv2D(channels[0], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P1)

    P1 = layers.Conv2D(num_classes, 1, activation="softmax")(P1)

    model = Model(inputs=inputs, outputs=P1)
    return model
