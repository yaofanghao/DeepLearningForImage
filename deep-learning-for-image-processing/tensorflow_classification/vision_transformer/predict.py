import os
import json
import glob
import numpy as np
import shutil

from PIL import Image
import tensorflow as tf
import matplotlib.pyplot as plt

from vit_model import vit_base_patch16_224_in21k as create_model

#------------------设置区域----------------------#
test_dir = "./test/IIM"
test_out_IIM_dir = "./out_IIM"
test_out_CIM_dir = "./out_CIM"

num_classes = 2
im_height = im_width = 224

if not os.path.exists(test_out_IIM_dir):
    os.makedirs(test_out_IIM_dir)
if not os.path.exists(test_out_CIM_dir):
    os.makedirs(test_out_CIM_dir)
#-------------------------------------------------#

path = os.path.join(test_dir)
img_list = os.listdir(path)

def main():
    for img in img_list:
        img_path = os.path.join(path,img)
        # img_path = "./test/CIM/陈一兵胃窦.jpg"
        assert os.path.exists(img_path), "file: '{}' dose not exist.".format(img_path)
        img = Image.open(img_path)
        img = img.resize((im_width, im_height))
        # plt.imshow(img)

        # read image
        img = np.array(img).astype(np.float32)

        # preprocess
        img = (img / 255. - 0.5) / 0.5

        # Add the image to a batch where it's the only member.
        img = (np.expand_dims(img, 0))

        # read class_indict
        json_path = './class_indices.json'
        assert os.path.exists(json_path), "file: '{}' dose not exist.".format(json_path)

        with open(json_path, "r") as f:
            class_indict = json.load(f)

        # create model
        model = create_model(num_classes=num_classes, has_logits=False)
        model.build([1, 224, 224, 3])

        weights_path = './save_weights/model.ckpt'
        assert len(glob.glob(weights_path+"*")), "cannot find {}".format(weights_path)
        model.load_weights(weights_path)

        result = np.squeeze(model.predict(img, batch_size=1))
        result = tf.keras.layers.Softmax()(result)
        predict_class = np.argmax(result)

        print(img_path)
        print(predict_class)
        print(result[predict_class])
        if predict_class == 0:
            shutil.copy(img_path,test_out_CIM_dir)
        if predict_class == 1:
            shutil.copy(img_path, test_out_IIM_dir)

        # print_res = "class: {}   prob: {:.3}".format(class_indict[str(predict_class)],
        #                                              result[predict_class])
        # plt.title(print_res)

        # for i in range(len(result)):
        #     print("class: {:10}   prob: {:.3}".format(class_indict[str(i)],
        #                                               result[i]))

        # plt.show()

if __name__ == '__main__':
    main()
