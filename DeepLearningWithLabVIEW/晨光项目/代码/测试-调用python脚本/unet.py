import colorsys
import copy
import numpy as np
from PIL import Image
from tensorflow.keras.layers import *
from tensorflow.keras.models import *
from tensorflow.keras import layers
from tensorflow.keras.initializers import RandomNormal

# 定义VGG，即5个block下采样结构
def VGG16(img_input):
    # Block 1
    # 512,512,3 -> 512,512,64
    x = layers.Conv2D(64, (3, 3),
                      activation='relu',
                      padding='same',
                      kernel_initializer=RandomNormal(stddev=0.02),
                      name='block1_conv1')(img_input)
    x = layers.Conv2D(64, (3, 3),
                      activation='relu',
                      padding='same',
                      kernel_initializer=RandomNormal(stddev=0.02),
                      name='block1_conv2')(x)
    feat1 = x
    # 512,512,64 -> 256,256,64
    x = layers.MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool')(x)

    # Block 2
    # 256,256,64 -> 256,256,128
    x = layers.Conv2D(128, (3, 3),
                      activation='relu',
                      padding='same',
                      kernel_initializer=RandomNormal(stddev=0.02),
                      name='block2_conv1')(x)
    x = layers.Conv2D(128, (3, 3),
                      activation='relu',
                      padding='same',
                      kernel_initializer=RandomNormal(stddev=0.02),
                      name='block2_conv2')(x)
    feat2 = x
    # 256,256,128 -> 128,128,128
    x = layers.MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool')(x)

    # Block 3
    # 128,128,128 -> 128,128,256
    x = layers.Conv2D(256, (3, 3),
                      activation='relu',
                      padding='same',
                      kernel_initializer=RandomNormal(stddev=0.02),
                      name='block3_conv1')(x)
    x = layers.Conv2D(256, (3, 3),
                      activation='relu',
                      padding='same',
                      kernel_initializer=RandomNormal(stddev=0.02),
                      name='block3_conv2')(x)
    x = layers.Conv2D(256, (3, 3),
                      activation='relu',
                      padding='same',
                      kernel_initializer=RandomNormal(stddev=0.02),
                      name='block3_conv3')(x)
    feat3 = x
    # 128,128,256 -> 64,64,256
    x = layers.MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool')(x)

    # Block 4
    # 64,64,256 -> 64,64,512
    x = layers.Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      kernel_initializer=RandomNormal(stddev=0.02),
                      name='block4_conv1')(x)
    x = layers.Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      kernel_initializer=RandomNormal(stddev=0.02),
                      name='block4_conv2')(x)
    x = layers.Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      kernel_initializer=RandomNormal(stddev=0.02),
                      name='block4_conv3')(x)
    feat4 = x
    # 64,64,512 -> 32,32,512
    x = layers.MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool')(x)

    # Block 5
    # 32,32,512 -> 32,32,512
    x = layers.Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      kernel_initializer=RandomNormal(stddev=0.02),
                      name='block5_conv1')(x)
    x = layers.Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      kernel_initializer=RandomNormal(stddev=0.02),
                      name='block5_conv2')(x)
    x = layers.Conv2D(512, (3, 3),
                      activation='relu',
                      padding='same',
                      kernel_initializer=RandomNormal(stddev=0.02),
                      name='block5_conv3')(x)
    feat5 = x
    return feat1, feat2, feat3, feat4, feat5

#定义UNET原始模型
def Unet_ori(input_shape=(512, 512, 3), num_classes=2):
    inputs = Input(input_shape)
    # -------------------------------#
    #   获得五个有效特征层
    #   feat1   512,512,64
    #   feat2   256,256,128
    #   feat3   128,128,256
    #   feat4   64,64,512
    #   feat5   32,32,512
    # -------------------------------#
    feat1, feat2, feat3, feat4, feat5 = VGG16(inputs)

    channels = [64, 128, 256, 512]

    # 32, 32, 512 -> 64, 64, 512
    P5_up = UpSampling2D(size=(2, 2))(feat5)
    # 64, 64, 512 + 64, 64, 512 -> 64, 64, 1024
    P4 = Concatenate(axis=3)([feat4, P5_up])
    # 64, 64, 1024 -> 64, 64, 512
    P4 = Conv2D(channels[3], 3, activation='relu', padding='same', kernel_initializer=RandomNormal(stddev=0.02))(P4)
    P4 = Conv2D(channels[3], 3, activation='relu', padding='same', kernel_initializer=RandomNormal(stddev=0.02))(P4)

    # 64, 64, 512 -> 128, 128, 512
    P4_up = UpSampling2D(size=(2, 2))(P4)
    # 128, 128, 256 + 128, 128, 512 -> 128, 128, 768
    P3 = Concatenate(axis=3)([feat3, P4_up])
    # 128, 128, 768 -> 128, 128, 256
    P3 = Conv2D(channels[2], 3, activation='relu', padding='same', kernel_initializer=RandomNormal(stddev=0.02))(P3)
    P3 = Conv2D(channels[2], 3, activation='relu', padding='same', kernel_initializer=RandomNormal(stddev=0.02))(P3)

    # 128, 128, 256 -> 256, 256, 256
    P3_up = UpSampling2D(size=(2, 2))(P3)
    # 256, 256, 256 + 256, 256, 128 -> 256, 256, 384
    P2 = Concatenate(axis=3)([feat2, P3_up])
    # 256, 256, 384 -> 256, 256, 128
    P2 = Conv2D(channels[1], 3, activation='relu', padding='same', kernel_initializer=RandomNormal(stddev=0.02))(P2)
    P2 = Conv2D(channels[1], 3, activation='relu', padding='same', kernel_initializer=RandomNormal(stddev=0.02))(P2)

    # 256, 256, 128 -> 512, 512, 128
    P2_up = UpSampling2D(size=(2, 2))(P2)
    # 512, 512, 128 + 512, 512, 64 -> 512, 512, 192
    P1 = Concatenate(axis=3)([feat1, P2_up])
    # 512, 512, 192 -> 512, 512, 64
    P1 = Conv2D(channels[0], 3, activation='relu', padding='same', kernel_initializer=RandomNormal(stddev=0.02))(P1)
    P1 = Conv2D(channels[0], 3, activation='relu', padding='same', kernel_initializer=RandomNormal(stddev=0.02))(P1)

    # 512, 512, 64 -> 512, 512, num_classes
    P1 = Conv2D(num_classes, 1, activation="softmax")(P1)

    model = Model(inputs=inputs, outputs=P1)
    return model

#   使用自己训练好的模型预测需要修改2个参数
#   model_path和num_classes都需要修改！
#   如果出现shape不匹配
#   一定要注意训练时的model_path和num_classes数的修改
class Unet(object):
    _defaults = {
        "model_path"        : "Epoch10-Total_Loss0.2388-Val_Loss0.1218.h5", #修改成自己训练的logs
        "model_image_size"  : (512, 512, 3),
        "num_classes"       : 2,
        # blend用于控制是否让识别结果和原图混合
        "blend"             : False,
    }

    # 初始化UNET
    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults)
        self.generate()

    #载入模型与权值
    def generate(self):
        self.model = Unet_ori(self.model_image_size, self.num_classes)
        self.model.load_weights(self.model_path)
        print('{} model loaded.'.format(self.model_path))
        
        if self.num_classes <= 21:
            self.colors = [(0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128), (0, 128, 128), 
                    (128, 128, 128), (64, 0, 0), (192, 0, 0), (64, 128, 0), (192, 128, 0), (64, 0, 128), (192, 0, 128), 
                    (64, 128, 128), (192, 128, 128), (0, 64, 0), (128, 64, 0), (0, 192, 0), (128, 192, 0), (0, 64, 128), (128, 64, 12)]
        else:
            # 画框设置不同的颜色
            hsv_tuples = [(x / len(self.class_names), 1., 1.)
                        for x in range(len(self.class_names))]
            self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
            self.colors = list(
                map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
                    self.colors))

    #不失真缩放
    def letterbox_image(self ,image, size):
        image = image.convert("RGB")
        iw, ih = image.size
        w, h = size
        scale = min(w/iw, h/ih)
        nw = int(iw*scale)
        nh = int(ih*scale)

        image = image.resize((nw,nh), Image.BICUBIC)
        new_image = Image.new('RGB', size, (128,128,128))
        new_image.paste(image, ((w-nw)//2, (h-nh)//2))
        return new_image,nw,nh

    #输入图片预测
    def detect_image(self, image):
        #---------------------------------------------------------#
        #   在这里将图像转换成RGB图像，防止灰度图在预测时报错。
        #---------------------------------------------------------#
        image = image.convert('RGB')
        
        #   对输入图像进行一个备份，后面用于绘图
        old_img = copy.deepcopy(image)
        orininal_h = np.array(image).shape[0]
        orininal_w = np.array(image).shape[1]

        #   进行不失真的resize，添加灰条，进行图像归一化
        img, nw, nh = self.letterbox_image(image,(self.model_image_size[1],self.model_image_size[0]))
        img = np.asarray([np.array(img)/255])
        
        #   图片传入网络进行预测
        pr = self.model.predict(img)[0]
        #   取出每一个像素点最大概率的种类
        pr = pr.argmax(axis=-1).reshape([self.model_image_size[0],self.model_image_size[1]])
        #   将灰条部分截取掉
        pr = pr[int((self.model_image_size[0]-nh)//2):int((self.model_image_size[0]-nh)//2+nh), int((self.model_image_size[1]-nw)//2):int((self.model_image_size[1]-nw)//2+nw)]

        #   创建一副新图，并根据每个像素点的种类赋予颜色
        seg_img = np.zeros((np.shape(pr)[0],np.shape(pr)[1],3))
        for c in range(self.num_classes):
            seg_img[:,:,0] += ((pr[:,: ] == c )*( self.colors[c][0] )).astype('uint8')
            seg_img[:,:,1] += ((pr[:,: ] == c )*( self.colors[c][1] )).astype('uint8')
            seg_img[:,:,2] += ((pr[:,: ] == c )*( self.colors[c][2] )).astype('uint8')

        #   将新图片转换成Image的形式
        image = Image.fromarray(np.uint8(seg_img)).resize((orininal_w,orininal_h), Image.NEAREST)

        #   将新图片和原图片混合
        if self.blend:
            image = Image.blend(old_img,image,0.7)
        return image

