from tensorflow.keras import layers
from tensorflow.keras.layers import *
from tensorflow.keras.models import Model
from nets.vgg16 import VGG16
# from tensorflow.python.keras.applications.mobilenet_v3 import hard_swish

from nets.mobilenet import relu6


def hard_sigmoid(x):
    return layers.ReLU(6.)(x+3)*(1./6.)
#
def hard_swish(x):
    return layers.Multiply()([hard_sigmoid(x),x])

#注意力机制
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

    # 组合成特征金字塔的结构
    # P5长宽共压缩了5次
    # Height/32,Width/32,256
    P_5 = Conv2D(256, (1, 1), name='fpn_c5p5')(C5)
    # P4长宽共压缩了4次
    # Height/16,Width/16,256
    P_4 = Add(name="fpn_p4add")([
        UpSampling2D(size=(2, 2), name="fpn_p5upsampled")(P_5),
        Conv2D(256, (1, 1), name='fpn_c4p4')(C4)])
    # P4长宽共压缩了3次
    # Height/8,Width/8,256
    P_3 = Add(name="fpn_p3add")([
        UpSampling2D(size=(2, 2), name="fpn_p4upsampled")(P_4),
        Conv2D(256, (1, 1), name='fpn_c3p3')(C3)])
    # P4长宽共压缩了2次
    # Height/4,Width/4,256
    P_2 = Add(name="fpn_p2add")([
        UpSampling2D(size=(2, 2), name="fpn_p3upsampled")(P_3),
        Conv2D(256, (1, 1), name='fpn_c2p2')(C2)])
    # 新增
    P_1 = Add(name="fpn_p1add")([
        UpSampling2D(size=(2, 2), name="fpn_p2upsampled")(P_2),
        Conv2D(256, (1, 1), name='fpn_c1p1')(C1)])

    # 各自进行一次256通道的卷积，此时P2、P3、P4、P5通道数相同
    # Height/2,Width/2,256
    feat1 = Conv2D(64, (3, 3), padding="SAME", name="fpn_p1")(P_1)
    x1 = squeeze(feat1)
    # Height/4,Width/4,256
    feat2 = Conv2D(128, (3, 3), padding="SAME", name="fpn_p2")(P_2)
    x2 = squeeze(feat2)
    # Height/8,Width/8,256
    feat3 = Conv2D(256, (3, 3), padding="SAME", name="fpn_p3")(P_3)
    x3 = squeeze(feat3)
    # Height/16,Width/16,256
    feat4 = Conv2D(512, (3, 3), padding="SAME", name="fpn_p4")(P_4)
    x4 = squeeze(feat4)
    # Height/32,Width/32,256
    feat5 = Conv2D(512, (3, 3), padding="SAME", name="fpn_p5")(P_5)

    channels = [64, 128, 256, 512]

    P5_up = UpSampling2D(size=(2, 2))(feat5)
    P4 = Concatenate(axis=3)([x4, P5_up])
    P4 = Conv2D(channels[3], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P4)
    P4 = Conv2D(channels[3], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P4)

    P4_up = UpSampling2D(size=(2, 2))(P4)
    P3 = Concatenate(axis=3)([x3, P4_up])
    P3 = Conv2D(channels[2], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P3)
    P3 = Conv2D(channels[2], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P3)

    P3_up = UpSampling2D(size=(2, 2))(P3)
    P2 = Concatenate(axis=3)([x2, P3_up])
    P2 = Conv2D(channels[1], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P2)
    P2 = Conv2D(channels[1], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P2)

    P2_up = UpSampling2D(size=(2, 2))(P2)
    P1 = Concatenate(axis=3)([x1, P2_up])
    P1 = Conv2D(channels[0], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P1)
    P1 = Conv2D(channels[0], 3, activation='relu', padding='same', kernel_initializer='he_normal')(P1)

    P1 = Conv2D(num_classes, 1, activation="softmax")(P1)

    model = Model(inputs=inputs, outputs=P1)
    return model
