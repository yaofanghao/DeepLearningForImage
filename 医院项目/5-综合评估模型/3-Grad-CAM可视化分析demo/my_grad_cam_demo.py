# 2023.3.22 
# 参考来源：
# https://github.com/keras-team/keras-io/blob/master/examples/vision/grad_cam.py

import numpy as np
import os
import tensorflow as tf
from tensorflow import keras
from IPython.display import Image, display
import matplotlib.pyplot as plt
import matplotlib.cm as cm

"""
## Configurable parameters

You can change these to another model.

To get the values for `last_conv_layer_name` use `model.summary()`
to see the names of all layers in the model.

"""

def get_img_array(img_path, size):
    # `img` is a PIL image of size 299x299
    img = keras.preprocessing.image.load_img(img_path, target_size=size)
    # `array` is a float32 Numpy array of shape (299, 299, 3)
    array = keras.preprocessing.image.img_to_array(img)
    # We add a dimension to transform our array into a "batch"
    # of size (1, 299, 299, 3)
    array = np.expand_dims(array, axis=0)
    return array

# gradcam 算法核心
def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    # First, we create a model that maps the input image to the activations
    # of the last conv layer as well as the output predictions
    grad_model = tf.keras.models.Model(
        [model.inputs], [model.get_layer(last_conv_layer_name).output, model.output]
    )

    # Then, we compute the gradient of the top predicted class for our input image
    # with respect to the activations of the last conv layer
    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    # This is the gradient of the output neuron (top predicted or chosen)
    # with regard to the output feature map of the last conv layer
    grads = tape.gradient(class_channel, last_conv_layer_output)

    # This is a vector where each entry is the mean intensity of the gradient
    # over a specific feature map channel
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # We multiply each channel in the feature map array
    # by "how important this channel is" with regard to the top predicted class
    # then sum all the channels to obtain the heatmap class activation
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    # For visualization purpose, we will also normalize the heatmap between 0 & 1
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()

# 保存和显示
def save_and_display_gradcam(img_path, heatmap, cam_path="cam.jpg", alpha=None):
    # Load the original image
    img = keras.preprocessing.image.load_img(img_path)
    img = keras.preprocessing.image.img_to_array(img)

    # Rescale heatmap to a range 0-255
    heatmap = np.uint8(255 * heatmap)

    # Use jet colormap to colorize heatmap
    jet = cm.get_cmap("jet")

    # Use RGB values of the colormap
    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap]

    # Create an image with RGB colorized heatmap
    jet_heatmap = keras.preprocessing.image.array_to_img(jet_heatmap)
    jet_heatmap = jet_heatmap.resize((img.shape[1], img.shape[0]))
    jet_heatmap = keras.preprocessing.image.img_to_array(jet_heatmap)

    # Superimpose the heatmap on original image
    # superimposed_img = jet_heatmap * alpha + img
    superimposed_img = jet_heatmap
    superimposed_img = keras.preprocessing.image.array_to_img(superimposed_img)

    # Save the superimposed image
    superimposed_img.save(cam_path)

    # Display Grad CAM
    # display(Image(cam_path))

if __name__ == "__main__":
    ################ 设置 ##############
    ####### 网络选择
    mode = "xception"
    # mode = "resnet50"

    ###### 图片文件夹所在路径选择
    dir_origin_path = 'img/'
    ######################################
    img_names = os.listdir(dir_origin_path)

    img_size = (299, 299)
    if mode=="xception":
        model_builder = keras.applications.xception.Xception
        preprocess_input = keras.applications.xception.preprocess_input
        decode_predictions = keras.applications.xception.decode_predictions
        last_conv_layer_name = "block14_sepconv2_act"
        flag = "xception"
    else:
        model_builder = keras.applications.resnet50.ResNet50
        preprocess_input = keras.applications.resnet50.preprocess_input
        last_conv_layer_name="conv5_block3_out"
        flag = "resnet50"

    dir_save_path = "img_out_" + flag + "/"
    if not os.path.exists(dir_save_path):
        os.makedirs(dir_save_path)

    # 导入模型
    model = model_builder(weights="imagenet")
    model.summary()

    for img_name in img_names:
        img_path = os.path.join(dir_origin_path, img_name)
        print("processing-----", img_name)

        # 处理图片
        img_array = preprocess_input(get_img_array(img_path, size=img_size))

        # 去除最后一层softmax
        model.layers[-1].activation = None

        # 输出预测最大概率的类别-针对xception
        # preds = model.predict(img_array)
        # print("Predicted:", decode_predictions(preds, top=1)[0])

        # 制作热力图
        heatmap = make_gradcam_heatmap(img_array, model, last_conv_layer_name)

        # 保存和显示热力图
        # plt.matshow(heatmap,cmap='OrRd')
        # plt.colorbar()
        # plt.show()

        cam_path = dir_save_path + img_name
        save_and_display_gradcam(img_path, heatmap, cam_path=cam_path, alpha=1)
