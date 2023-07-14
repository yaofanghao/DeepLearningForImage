
import tensorflow as tf
from nets.hrnet import HRnet

if __name__ == "__main__":
    input_shape = [480, 480]
    num_classes = 9
    backbone = 'hrnetv2_w32'

    model = HRnet([input_shape[0], input_shape[1], 3], num_classes, backbone=backbone)
    # --------------------------------------------#
    #   查看网络结构网络结构
    model.summary()

    # --------------------------------------------#
    #   获得网络每个层的名称与序号
    # for i,layer in enumerate(model.layers):
    #     print(i,layer.name)

    model_path = 'logs_7_12.h5'  # 模型文件

    # model = tf.keras.models.load_model(model_path)
    # 如果报错，解决方法：
    # 训练时，save_weights_only都应改成False！
    # https://blog.csdn.net/QAQIknow/article/details/123182184
    # custom_objects={'UpsampleLike':UpsampleLike}

    # 转为pb模型
    model.save('_hrnet', save_format='tf')

    # https://blog.csdn.net/qq_16792139/article/details/126058843
    # pb模型转为onnx的命令
    '''
    python -m tf2onnx.convert --saved-model ./_hrnet --output hrnet.onnx --opset 11 --verbose
    '''

