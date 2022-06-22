#打印模型png图示例
from keras.applications.resnet import ResNet50
from keras.utils.vis_utils import plot_model

if __name__ == "__main__":
    model = ResNet50(weights='imagenet')
    model.summary()

    for i,layer in enumerate(model.layers):  #打印层数信息
        print(i,layer.name)

    plot_model(model, show_shapes=True, to_file='model.png' )  #打印模型png图