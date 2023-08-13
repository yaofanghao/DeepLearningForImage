"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/7/13 11:04
    @Filename: my_onnx_test.py
    @Software: PyCharm     
"""

import numpy as np
import cv2
import colorsys
from PIL import Image, ImageFont, ImageDraw
from utils.utils import (cvtColor, preprocess_input)
from utils.utils_bbox import DecodeBoxNP
import onnxruntime

import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


class YOLO_ONNX(object):
    def __init__(self, model_name):
        self.onnx_path = model_name

        # 2023.8.13 classes_path 如果改成中文的标签，画框显示时类别就是中文的
        self.classes_path = "class_name_gbk.txt"

        self.anchors_path = "yolo_anchors.txt"
        self.anchors_mask = [[6, 7, 8], [3, 4, 5], [0, 1, 2]]
        self.input_shape = [640, 640]
        self.confidence = 0.5
        self.nms_iou = 0.3
        self.letterbox_image = True

        self.onnx_session = onnxruntime.InferenceSession(self.onnx_path)
        # 获得所有的输入node
        self.input_name = self.get_input_name()
        # 获得所有的输出node
        self.output_name = self.get_output_name()

        # ---------------------------------------------------#
        #   获得种类和先验框的数量
        # ---------------------------------------------------#
        self.class_names, self.num_classes = self.get_classes(self.classes_path)
        self.anchors, self.num_anchors = self.get_anchors(self.anchors_path)
        self.bbox_util = DecodeBoxNP(self.anchors, self.num_classes, (self.input_shape[0], self.input_shape[1]),
                                     self.anchors_mask)

        # ---------------------------------------------------#
        #   画框设置不同的颜色
        # ---------------------------------------------------#
        hsv_tuples = [(x / self.num_classes, 1., 1.) for x in range(self.num_classes)]
        self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        self.colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), self.colors))

    def get_classes(self, classes_path):
        with open(classes_path, encoding='utf-8') as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names, len(class_names)

    def get_anchors(self, anchors_path):
        with open(anchors_path, encoding='utf-8') as f:
            anchors = f.readline()
        anchors = [float(x) for x in anchors.split(',')]
        anchors = np.array(anchors).reshape(-1, 2)
        return anchors, len(anchors)

    def get_input_name(self):
        # 获得所有的输入node
        input_name = []
        for node in self.onnx_session.get_inputs():
            input_name.append(node.name)
        return input_name

    def get_output_name(self):
        # 获得所有的输出node
        output_name = []
        for node in self.onnx_session.get_outputs():
            output_name.append(node.name)
        return output_name

    def get_input_feed(self, image_tensor):
        # 利用input_name获得输入的tensor
        input_feed = {}
        for name in self.input_name:
            input_feed[name] = image_tensor
        return input_feed

    # ---------------------------------------------------#
    #   对输入图像进行resize
    # ---------------------------------------------------#
    def resize_image(self, image, size, mode='PIL'):
        if mode == 'PIL':
            iw, ih = image.size
            w, h = size

            scale = min(w / iw, h / ih)
            nw = int(iw * scale)
            nh = int(ih * scale)

            image = image.resize((nw, nh), Image.BICUBIC)
            new_image = Image.new('RGB', size, (128, 128, 128))
            new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))

        else:
            image = np.array(image)
            # 获得现在的shape
            shape = np.shape(image)[:2]
            # 获得输出的shape
            if isinstance(size, int):
                size = (size, size)

            # 计算缩放的比例
            r = min(size[0] / shape[0], size[1] / shape[1])

            # 计算缩放后图片的高宽
            new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
            dw, dh = size[1] - new_unpad[0], size[0] - new_unpad[1]

            # 除以2以padding到两边
            dw /= 2
            dh /= 2

            # 对图像进行resize
            if shape[::-1] != new_unpad:  # resize
                image = cv2.resize(image, new_unpad, interpolation=cv2.INTER_LINEAR)
            top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
            left, right = int(round(dw - 0.1)), int(round(dw + 0.1))

            new_image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT,
                                           value=(128, 128, 128))  # add border

        return new_image

    def detect_image(self, image):
        image_shape = np.array(np.shape(image)[0:2])
        # ---------------------------------------------------------#
        #   在这里将图像转换成RGB图像，防止灰度图在预测时报错。
        #   代码仅仅支持RGB图像的预测，所有其它类型的图像都会转化成RGB
        # ---------------------------------------------------------#
        image = cvtColor(image)

        image_data = self.resize_image(image, self.input_shape, True)
        # ---------------------------------------------------------#
        #   添加上batch_size维度
        #   h, w, 3 => 3, h, w => 1, 3, h, w
        # ---------------------------------------------------------#
        image_data = np.expand_dims(np.transpose(preprocess_input(np.array(image_data, dtype='float32')), (2, 0, 1)), 0)

        input_feed = self.get_input_feed(image_data)
        outputs = self.onnx_session.run(output_names=self.output_name, input_feed=input_feed)

        logging.info("predict done")

        feature_map_shape = [[int(j / (2 ** (i + 3))) for j in self.input_shape] for i in
                             range(len(self.anchors_mask))][::-1]
        for i in range(len(self.anchors_mask)):
            outputs[i] = np.reshape(outputs[i],
                                    (1, len(self.anchors_mask[i]) * (5 + self.num_classes),
                                     feature_map_shape[i][0], feature_map_shape[i][1]))

        outputs = self.bbox_util.decode_box(outputs)
        # ---------------------------------------------------------#
        #   将预测框进行堆叠，然后进行非极大抑制
        # ---------------------------------------------------------#
        results = self.bbox_util.non_max_suppression(np.concatenate(outputs, 1), self.num_classes, self.input_shape,
                                                     image_shape, self.letterbox_image, conf_thres=self.confidence,
                                                     nms_thres=self.nms_iou)

        # 2023.8.12 没有预测结果时，修改返回值为空的数组out_scores和out_classes，防止程序报错
        if results[0] is None:
            return image, np.array([]), np.array([])

        top_label = np.array(results[0][:, 6], dtype='int32')
        top_conf = results[0][:, 4] * results[0][:, 5]
        top_boxes = results[0][:, :4]

        # ---------------------------------------------------------#
        #   设置字体与边框厚度
        # ---------------------------------------------------------#
        font = ImageFont.truetype(font='model_data/simhei.ttf',
                                  size=np.floor(3e-2 * image.size[1] + 8).astype('int32'))
        thickness = int(max((image.size[0] + image.size[1]) // np.mean(self.input_shape), 1))

        # ---------------------------------------------------------#
        #   图像绘制
        # ---------------------------------------------------------#
        for i, c in list(enumerate(top_label)):
            predicted_class = self.class_names[int(c)]

            box = top_boxes[i]
            score = top_conf[i]

            top, left, bottom, right = box

            top = max(0, np.floor(top).astype('int32'))
            left = max(0, np.floor(left).astype('int32'))
            bottom = min(image.size[1], np.floor(bottom).astype('int32'))
            right = min(image.size[0], np.floor(right).astype('int32'))

            label = '{} {:.2f}'.format(predicted_class, score)
            draw = ImageDraw.Draw(image)
            label_size = draw.textsize(label, font)
            label = label.encode('utf-8')
            print(label, top, left, bottom, right)

            if top - label_size[1] >= 0:
                text_origin = np.array([left, top - label_size[1]])
            else:
                text_origin = np.array([left, top + 1])

            for i in range(thickness):
                draw.rectangle([left + i, top + i, right - i, bottom - i], outline=self.colors[c])
            draw.rectangle([tuple(text_origin), tuple(text_origin + label_size)], fill=self.colors[c])
            draw.text(text_origin, str(label, 'UTF-8'), fill=(0, 0, 0), font=font)
            del draw

        return image, top_conf, top_label

if __name__ == "__main__":
    model_name = "yolov5_x.onnx"
    img_name = "xiu1.jpg"

    yolo = YOLO_ONNX(model_name=model_name)

    logging.info("load image")
    image = Image.open(img_name)

    r_image, _, _ = yolo.detect_image(image)
    logging.info("success")

    r_image.show()

