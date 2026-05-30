# 2023.3.22
# 参考来源：
# https://github.com/keras-team/keras-io/blob/master/examples/vision/grad_cam.py

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.cm as cm

"""
Grad-CAM 热力图可视化工具。
支持 Xception、ResNet50、Faster-RCNN 三种网络。
"""

# ==================== 默认参数 ====================
_HEATMAP_ALPHA = 1.0  # 热力图叠加透明度
# =================================================

# 网络配置映射：mode -> (img_size, model_builder, preprocess_input, last_conv_layer_name)
_MODEL_CONFIGS = {
    "xception": {
        "img_size": (299, 299),
        "model_builder": keras.applications.xception.Xception,
        "preprocess_input": keras.applications.xception.preprocess_input,
        "last_conv_layer_name": "block14_sepconv2_act",
    },
    "resnet50": {
        "img_size": (224, 224),
        "model_builder": keras.applications.resnet50.ResNet50,
        "preprocess_input": keras.applications.resnet50.preprocess_input,
        "last_conv_layer_name": "conv5_block2_out",
    },
}


def get_img_array(img_path, size):
    """读取图片并转为模型输入格式的 numpy 数组。"""
    img = keras.preprocessing.image.load_img(img_path, target_size=size)
    array = keras.preprocessing.image.img_to_array(img)
    array = np.expand_dims(array, axis=0)
    return array


def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    """Grad-CAM 算法核心：生成类别激活热力图。"""
    grad_model = tf.keras.models.Model(
        [model.inputs],
        [model.get_layer(last_conv_layer_name).output, model.output],
    )

    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    grads = tape.gradient(class_channel, last_conv_layer_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()


def save_and_display_gradcam(img_path, heatmap, cam_path="cam.jpg", alpha=None):
    """将热力图叠加到原图上并保存。"""
    if alpha is None:
        alpha = _HEATMAP_ALPHA

    img = keras.preprocessing.image.load_img(img_path)
    img = keras.preprocessing.image.img_to_array(img)

    heatmap = np.uint8(255 * heatmap)
    jet = cm.get_cmap("jet")
    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap]

    jet_heatmap = keras.preprocessing.image.array_to_img(jet_heatmap)
    jet_heatmap = jet_heatmap.resize((img.shape[1], img.shape[0]))
    jet_heatmap = keras.preprocessing.image.img_to_array(jet_heatmap)

    superimposed_img = jet_heatmap * alpha + img
    superimposed_img = keras.preprocessing.image.array_to_img(superimposed_img)
    superimposed_img.save(cam_path)


def _setup_frcnn(num_classes=3, input_shape=(600, 600)):
    """加载 Faster-RCNN 模型用于 Grad-CAM."""
    from nets.frcnn import get_model
    _, model = get_model(num_classes, 'resnet', input_shape=[*input_shape, 3])
    return model, "bn4f_branch2c"


if __name__ == "__main__":
    # ==================== 设置 ====================
    mode = "xception"     # 可选: "xception" / "resnet50" / "frcnn"
    dir_origin_path = "img/"   # 待处理图片所在文件夹
    # ==============================================

    if not os.path.exists(dir_origin_path):
        print(f"错误：文件夹不存在 {dir_origin_path}")
        exit(1)

    img_names = os.listdir(dir_origin_path)

    if mode in _MODEL_CONFIGS:
        cfg = _MODEL_CONFIGS[mode]
        img_size = cfg["img_size"]
        preprocess_input = cfg["preprocess_input"]
        last_conv_layer_name = cfg["last_conv_layer_name"]
        model = cfg["model_builder"](weights="imagenet")
    elif mode == "frcnn":
        img_size = (600, 600)
        preprocess_input = keras.applications.resnet50.preprocess_input
        model, last_conv_layer_name = _setup_frcnn()
    else:
        print(f"错误：不支持的 mode '{mode}'，可选: {list(_MODEL_CONFIGS.keys()) + ['frcnn']}")
        exit(1)

    dir_save_path = f"img_out_{mode}_{last_conv_layer_name}/"
    if not os.path.exists(dir_save_path):
        os.makedirs(dir_save_path)

    # 去除最后一层 softmax，获得原始 logits
    model.layers[-1].activation = None

    for img_name in img_names:
        img_path = os.path.join(dir_origin_path, img_name)
        print("processing-----", img_name)

        img_array = preprocess_input(get_img_array(img_path, size=img_size))
        heatmap = make_gradcam_heatmap(img_array, model, last_conv_layer_name)

        cam_path = os.path.join(dir_save_path, img_name)
        save_and_display_gradcam(img_path, heatmap, cam_path=cam_path)

    print("完成！结果保存至:", dir_save_path)
