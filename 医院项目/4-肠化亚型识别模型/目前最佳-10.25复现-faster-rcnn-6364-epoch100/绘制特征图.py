"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2024/1/15 14:31
    @Filename: 绘制特征图.py
    @Software: PyCharm     
"""

'''
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from nets.frcnn import get_model
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from keras.applications.imagenet_utils import preprocess_input
from utils.utils import (cvtColor, get_classes, get_new_img_size, resize_image,
                         show_config)

########################
weights_path = 'logs/best_epoch_weights.h5'
image_path = '1.jpg'
########################

input_shape = [600, 600]
num_classes = 3

_, model = get_model(num_classes, 'resnet50',
                     input_shape=[input_shape[0], input_shape[1], 3])

model.load_weights(weights_path)

image = Image.open(image_path)
image_shape = np.array(np.shape(image)[0:2])
input_shape = get_new_img_size(image_shape[0], image_shape[1])

image = cvtColor(image)
image_data = resize_image(image, [input_shape[1], input_shape[0]])
# image_data = np.expand_dims(preprocess_input(np.array(image_data, dtype='float32')), 0)

layer_name = 'roi_pooling_conv'  # 指定要获取特征图的层的名称
intermediate_layer_model = tf.keras.Model(inputs=model.input,
                                         outputs=model.get_layer(layer_name).output)

image_array = img_to_array(image_data)
image_tensor = tf.convert_to_tensor(image_array, dtype=tf.float32)
intermediate_output = intermediate_layer_model(image_tensor)

# 将特征图可视化
feature_map = np.squeeze(intermediate_output.numpy(), axis=0)  # 去除批次维度

plt.imshow(feature_map, cmap='gray')
plt.show()
'''

'''
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
import os

image_path = '1.jpg'
filename, _ = os.path.splitext(image_path)

model = ResNet50(weights='imagenet')
layer_outputs = [layer.output for layer in model.layers[1:]]  # 获取所有层的输出
activation_model = tf.keras.models.Model(inputs=model.input, outputs=layer_outputs)  # 创建新的模型

image = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
input_image = tf.keras.preprocessing.image.img_to_array(image)
input_image = np.expand_dims(input_image, axis=0)
input_image = preprocess_input(input_image)

activations = activation_model.predict(input_image)
save_folder = 'result_' + filename + '/'
os.makedirs(save_folder, exist_ok=True)

residual_outputs = activation_model.predict(input_image)

rows = int(np.sqrt(len(activations)))  # 计算行数，假设特征图数量是平方数
cols = len(activations) // rows  # 计算列数
fig, axes = plt.subplots(rows, cols, figsize=(10, 10))

# 遍历并绘制每一个特征图
for i, activation in enumerate(activations):
    row = i // cols
    col = i % cols
    axes[row, col].matshow(activation[0, :, :, 0], cmap='viridis')
    axes[row, col].set_title(f"Layer {i+1}")
    axes[row, col].axis('off')

# 移除多余的子图
if len(activations) < (rows * cols):
    for j in range(len(activations), rows * cols):
        axes.flat[j].set_visible(False)

save_path = os.path.join(save_folder, "result.png")
axes.savefig(save_path)

plt.tight_layout()
plt.show()
'''


import numpy as np
import torch
import matplotlib.pyplot as plt
from PIL import Image
from torchvision import models, transforms

model = models.resnet50(pretrained=True)

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

image = transform(Image.open('1.jpg')).unsqueeze(0)

features = model.conv1(image)
feature_map = features[0].detach().numpy()

row = 8
col = 8

fig, ax = plt.subplots(row, col, figsize=(10, 10))
for i in range(row):
    for j in range(col):
        ax[i, j].imshow(feature_map[i * col + j], cmap='viridis')
        ax[i, j].axis('off')
plt.show()



