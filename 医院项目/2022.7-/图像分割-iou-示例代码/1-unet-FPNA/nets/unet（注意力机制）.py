import numpy as np
from tensorflow.keras.layers import Conv2D, Input, MaxPooling2D, Dropout, concatenate, UpSampling2D
from keras.models import *
from keras.layers import *
from nets.mobilenet import relu6
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.applications.mobilenet_v3 import hard_swish
from nets.vgg16 import VGG16

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
    feat1, feat2, feat3, feat4, feat5 = VGG16(inputs)

    channels = [64, 128, 256, 512]

    P5_up = UpSampling2D(size=(2, 2))(feat5)
    P4 = Concatenate(axis=3)([feat4, P5_up])
    P4 = squeeze(P4)
    P4 = Conv2D(channels[3], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P4)
    P4 = Conv2D(channels[3], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P4)

    P4_up = UpSampling2D(size=(2, 2))(P4)
    P3 = Concatenate(axis=3)([feat3, P4_up])
    P3 = squeeze(P3)
    P3 = Conv2D(channels[2], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P3)
    P3 = Conv2D(channels[2], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P3)

    P3_up = UpSampling2D(size=(2, 2))(P3)
    P2 = Concatenate(axis=3)([feat2, P3_up])
    P2 = squeeze(P2)
    P2 = Conv2D(channels[1], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P2)
    P2 = Conv2D(channels[1], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P2)

    P2_up = UpSampling2D(size=(2, 2))(P2)
    P1 = Concatenate(axis=3)([feat1, P2_up])
    P1 = squeeze(P1)
    P1 = Conv2D(channels[0], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P1)
    P1 = Conv2D(channels[0], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P1)

    P1 = Conv2D(num_classes, 1, activation="softmax")(P1)

    model = Model(inputs=inputs, outputs=P1)
    return model
