"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/7/13 11:04
    @Filename: my_onnx_test.py
    @Software: PyCharm     
"""

# 2023.8.11-更改为 yolo-onnx模型推理
# 2023.8.15-增加预测结果存储到txt和数据库mdb中的功能

import os
import numpy as np
import cv2
import colorsys
from PIL import Image, ImageFont, ImageDraw
from utils.utils import (cvtColor, preprocess_input)
from utils.utils_bbox import DecodeBoxNP
import pyodbc
from datetime import datetime
import onnxruntime
import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


# #########################参数设置区域
argparse_txt = "argparse.txt"  # 配置参数文件
current_dir = os.path.dirname(os.path.abspath(__file__))
db_file_path = os.path.join(current_dir, 'predict_result.mdb')  # 构造数据库文件，并连接到Access数据库，DBQ需要是绝对路径
table_name = "result"

def load_arg():
    # 方法二 以读取配置文件argparse.txt的方式载入参数
    # 配置参数说明：
    # lines_arg[0]为预测模式 0或1 0为单张图片预测 1为视频预测 默认为1
    # lines_arg[1]为视频帧计数间隔频率 影响视频检测速率，可任意设置，建议值10-30之间
    # lines_arg[2]为待检测图片\视频的相对路径
    # lines_arg[3]为地点
    # lines_arg[4]为检测人
    # lines_arg[5]为产品代号
    # lines_arg[6]为批次号
    # lines_arg[7]为备注

    f_arg = open(argparse_txt, "r",  encoding='utf-8')
    lines_arg = f_arg.read().splitlines()
    logging.info("success load arg from: {}".format(argparse_txt))
    logging.info("setting mode: {} \t  timeF:{} "
                 .format(lines_arg[0], lines_arg[1]))
    logging.info("success read filename: {} \t".format(lines_arg[2]))
    return lines_arg[0], lines_arg[1], lines_arg[2], \
        lines_arg[3], lines_arg[4], \
        lines_arg[5], lines_arg[6], lines_arg[7]


def table_exists(table_name, db_file_path):
    conn_str = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + db_file_path
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # 获取数据库中的所有表
    tables = cursor.tables(tableType='TABLE')

    # 遍历表列表，判断特定表是否存在
    for table in tables:
        if table.table_name == table_name:
            cursor.close()
            conn.close()
            return True

    cursor.close()
    conn.close()
    return False


class YoloOnnx(object):
    def __init__(self, model_name):
        self.onnx_path = model_name
        self.classes_path = os.path.join(current_dir, "class_name_gbk.txt")
        self.anchors_path = os.path.join(current_dir, "yolo_anchors.txt")
        self.anchors_mask = [[6, 7, 8], [3, 4, 5], [0, 1, 2]]
        self.input_shape = [640, 640]
        self.confidence = 0.8
        self.nms_iou = 0.3
        self.letterbox_image = True

        self.onnx_session = onnxruntime.InferenceSession(self.onnx_path)

        # 获得所有的输入和输出node
        self.input_name = self.get_input_name()
        self.output_name = self.get_output_name()

        #   获得种类和先验框的数量
        self.class_names, self.num_classes = self.get_classes(self.classes_path)
        self.anchors, self.num_anchors = self.get_anchors(self.anchors_path)
        self.bbox_util = DecodeBoxNP(self.anchors, self.num_classes, (self.input_shape[0], self.input_shape[1]),
                                     self.anchors_mask)

        #   画框设置不同的颜色
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

    #   对输入图像进行resize
    def resize_image(self, image, size):
        image = np.array(image)
        shape = np.shape(image)[:2]  # 获得现在的shape
        if isinstance(size, int):  # 获得输出的shape
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
        if shape[::-1] != new_unpad:
            image = cv2.resize(image, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))

        # 添加border
        new_image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT,
                                       value=(128, 128, 128))
        return new_image

    def detect_image(self, image):
        image_shape = np.array(np.shape(image)[0:2])

        #   在这里将图像转换成RGB图像，防止灰度图在预测时报错
        image = cvtColor(image)
        image_data = self.resize_image(image, self.input_shape)

        #   添加上batch_size维度
        #   h, w, 3 => 3, h, w => 1, 3, h, w
        image_data = np.expand_dims(np.transpose(preprocess_input(np.array(image_data, dtype='float32')), (2, 0, 1)), 0)

        #   传入onnx模型预测
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

        #   将预测框进行堆叠，然后进行非极大抑制
        results = self.bbox_util.non_max_suppression(np.concatenate(outputs, 1), self.num_classes, self.input_shape,
                                                     image_shape, self.letterbox_image, conf_thres=self.confidence,
                                                     nms_thres=self.nms_iou)

        #   2023.8.12
        #   没有预测结果时，修改返回值为空的数组out_scores和out_classes，防止程序报错
        if results[0] is None:
            return image, np.array([]), np.array([])

        top_label = np.array(results[0][:, 6], dtype='int32')
        top_conf = results[0][:, 4] * results[0][:, 5]
        top_boxes = results[0][:, :4]

        #   设置字体与边框厚度
        font = ImageFont.truetype(font='simhei.ttf', size=np.floor(3e-2 * image.size[1] + 8).astype('int32'))
        thickness = int(max((image.size[0] + image.size[1]) // np.mean(self.input_shape), 1))

        #   图像绘制
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

            for j in range(thickness):
                draw.rectangle([left + j, top + j, right - j, bottom - j], outline=self.colors[c])
            draw.rectangle([tuple(text_origin), tuple(text_origin + label_size)], fill=self.colors[c])
            draw.text(text_origin, str(label, 'UTF-8'), fill=(0, 0, 0), font=font)
            del draw

        return image, top_conf, top_label


def load(onnx_model_name):
    yolo = YoloOnnx(model_name=onnx_model_name)
    return yolo


def onnx_predict(img_name, onnx_,
                 output_path):

    image_full_path = os.path.join(current_dir, str(img_name))
    image = Image.open(image_full_path)
    img_name_single = img_name.rsplit("\\", 1)[-1]
    file_name = 'camera'
    _name_classes_gbk = ['背景', '多余物','氧化物',
                         '鼓波', '划伤', '起皮',
                         '锈斑', '凹坑', '焊接缺陷']

    result_txt = open(str(output_path + 'camera_predict_result.txt'), 'a')

    #   2023.8.11
    #   修改返回值，包括图片、分数、类别
    logging.info("time1")
    r_image, out_scores, out_classes = onnx_.detect_image(image)
    logging.info("time2")

    #  这张图要有检测结果才进入该循环，进行数据库存储、预测图片保存等操作
    if out_scores.size != 0:

        #   2023.3.3
        #   只保存有预测结果的图片（只有background不算作有预测结果）
        result_txt.write(img_name_single)
        result_txt.write("\r")
        insert_detect_result = ""

        for i in range(out_classes.shape[0]):
            if out_classes[i] > 0:
                temp = out_classes[i]
                logging.info("识别出：{}--{}".format(temp, _name_classes_gbk[temp]))
                insert_detect_result = insert_detect_result + str(_name_classes_gbk[temp]) + str(np.round(out_scores[i], 4)) + ", "
        result_txt.write(insert_detect_result)

        result_txt.write("\r")
        result_txt.write("\r")

        #   保存预测图片，写入预测结果到txt中
        r_image.save(str(os.path.join(output_path, img_name_single)),
                     quality=95, subsampling=0)

    logging.info("success")
    # r_image.show()
    result_txt.close()
    # conn.close()
    return 1


def save_video(output_path, fps):
    # 输入文件夹和输出视频文件名
    output_video = output_path + '\\output.mp4'  # 输出视频文件名

    image_files = sorted([os.path.join(output_path, file) for file in os.listdir(output_path)
                          if file.endswith(".jpg")],
                         key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))

    # 加载第一张图像获取大小信息
    first_image = cv2.imread(image_files[0])
    height, width, _ = first_image.shape

    # 创建视频编写器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    for image_file in image_files:
        image = cv2.imread(image_file)
        video_writer.write(image)
        logging.info("success save {} to {}".format(image_file, output_video))

    video_writer.release()
    logging.info("success save to video")

    return 1

def save_to_database(output_path=None):
    print("1+1")

    f_arg = open(os.path.join(current_dir, "argparse.txt"), "r", encoding="utf-8")
    lines_arg = f_arg.read().splitlines()
    logging.info("success load arg from: {}".format(argparse_txt))
    logging.info("setting mode: {} \t  timeF:{} "
                 .format(lines_arg[0], lines_arg[1]))
    logging.info("success read filename: {} \t".format(lines_arg[2]))

    _mode, _timeF, _filename, _location, _people, _pipe_number, _pici_number, _comment =     \
        lines_arg[0], lines_arg[1], lines_arg[2], \
        lines_arg[3], lines_arg[4], \
        lines_arg[5], lines_arg[6], lines_arg[7]

    # # 连接数据库
    conn_str = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + str(db_file_path)
    logging.info("成功创建并打开数据库，路径为{}".format(db_file_path))
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    if not table_exists(table_name=table_name, db_file_path=db_file_path):
        create_table_sql = '''
            CREATE TABLE {} (
                时间 DATETIME,
                地点 VARCHAR(50),
                检测人 VARCHAR(50),
                产品代号 VARCHAR(50),
                批次号 VARCHAR(50),
                图片名 VARCHAR(50),
                检测结果 VARCHAR(50),
                备注 VARCHAR(50)
            )
        '''.format(table_name)
        cursor.execute(create_table_sql)
        logging.info("创建完成！")
    if table_exists(table_name=table_name, db_file_path=db_file_path):
        logging.info("已有表！")

    result_txt = str(output_path + 'camera_predict_result.txt')

    with open(result_txt, 'r') as file:
        lines = file.readlines()  # 逐行读取文件内容，并将每行存储在列表中

    for i in range(0, len(lines), 3):  # 按照每隔一行的间隔遍历列表
        print(i)
        img_name_single = lines[i].strip()  # 获取当前行的内容，并去除首尾的空白字符
        insert_detect_result = lines[i + 1].strip()
        print(img_name_single)
        print(insert_detect_result)

        insert_data_sql = '''
            INSERT INTO {} VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''.format(table_name)
        values = (datetime.now(), _location, _people,
                  _pipe_number, _pici_number, "camera_"+img_name_single, insert_detect_result,
                  _comment)
        cursor.execute(insert_data_sql, values)
    conn.commit()

    #   关闭数据库连接
    cursor.close()

    return 1

# if __name__ == "__main__":
#
#     base_dir = "C:\\Users\\Rainy\\Desktop\\project-2022-64bit-yolov5-20231031\\"
#     model_name = base_dir + "yolov5_s.onnx"
#     img_name = base_dir + "1.jpg"
#     output_path = base_dir + "img_out\\"
#     # if not os.path.exists(output_path):
#     #     os.makedirs(output_path)
#     #
#     # logging.info("load image")
#     #
#     # # 只在labview初始化时候，调用一次load函数
#     # onnx_ = load(onnx_model_name=model_name)
#     #
#     # logging.info("time0")
#     # # 在labview的while循环中处理detect_image函数
#     # onnx_predict(img_name=img_name, onnx_=onnx_,
#     #              output_path=output_path)
#     # logging.info("time3")
#
#     save_to_database(output_path=output_path)
#     logging.info("time4")
#
#     # 合成img_out中的图片为视频
#     # fps = 2  # 保存视频的帧率
#     # save_video(output_path, fps)
