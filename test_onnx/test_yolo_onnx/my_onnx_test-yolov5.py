"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/7/13 11:04
    @Filename: my_onnx_test.py
    @Software: PyCharm     
"""

# 2023.7.20-补充 mode=2时 摄像头读取功能
# 2023.8.11-补充 增加数据库保存信息，如地点、检测人、软管序号等
# 2023.8.11-更改为 yolo-onnx模型推理

import os
from tqdm import tqdm
import numpy as np
import cv2
import colorsys
from PIL import Image, ImageFont, ImageDraw
import pyodbc
from datetime import datetime

from utils.utils import (cvtColor, preprocess_input, show_config)
from utils.utils_bbox import DecodeBoxNP

import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


# #########################参数设置区域
_classes_txt = "class_name.txt"  # 分类标签文件
_classes_gbk_txt = "class_name_gbk.txt"  # 分类标签文件中文版
argparse_txt = "argparse.txt"  # 配置参数文件
current_dir = os.path.dirname(os.path.abspath(__file__))
db_file_path = os.path.join(current_dir, 'predict_result.mdb')  # 构造数据库文件，并连接到Access数据库，DBQ需要是绝对路径

model_name = "yolov5_x.onnx"
num_classes = 9  # 分类类别 八类+背景一类


def load_arg():
    # 方法二 以读取配置文件argparse.txt的方式载入参数
    # 配置参数说明：
    # lines_arg[0]为预测模式 0或1 0为单张图片预测 1为视频预测 默认为1
    # lines_arg[1]为视频帧计数间隔频率 影响视频检测速率，可任意设置，建议值10-30之间
    # lines_arg[2]为待检测图片\视频的相对路径
    # lines_arg[3]为地点
    # lines_arg[4]为检测人
    # lines_arg[5]为软管序号
    # lines_arg[6]为备注

    f_arg = open(argparse_txt, "r", encoding='gbk')
    lines_arg = f_arg.read().splitlines()
    logging.info("success load arg from: {}".format(argparse_txt))
    logging.info("setting mode: {} \t  timeF:{} "
                 .format(lines_arg[0], lines_arg[1]))
    logging.info("success read filename: {} \t".format(lines_arg[2]))
    return lines_arg[0], lines_arg[1], lines_arg[2], \
        lines_arg[3], lines_arg[4], \
        lines_arg[5], lines_arg[6]


def read_txt_lines(_classes_txt=None, _classes_gbk_txt=None):
    __name_classes = []
    __name_classes_gbk = []
    f = open(_classes_txt, "r")
    f_gbk = open(_classes_gbk_txt, "r", encoding='utf-8')
    lines = f.read().splitlines()
    lines_gbk = f_gbk.read().splitlines()
    for i in range(len(lines)):
        __name_classes.append(lines[i])
        __name_classes_gbk.append(lines_gbk[i])
    return __name_classes, __name_classes_gbk


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


class YOLO_ONNX(object):
    _defaults = {
        # --------------------------------------------------------------------------#
        #   使用自己训练好的模型进行预测一定要修改onnx_path和classes_path！
        #   onnx_path指向logs文件夹下的权值文件，classes_path指向model_data下的txt
        #
        #   训练好后logs文件夹下存在多个权值文件，选择验证集损失较低的即可。
        #   验证集损失较低不代表mAP较高，仅代表该权值在验证集上泛化性能较好。
        #   如果出现shape不匹配，同时要注意训练时的onnx_path和classes_path参数的修改
        # --------------------------------------------------------------------------#
        "onnx_path": model_name,
        "classes_path": 'class_name.txt',
        # ---------------------------------------------------------------------#
        #   anchors_path代表先验框对应的txt文件，一般不修改。
        #   anchors_mask用于帮助代码找到对应的先验框，一般不修改。
        # ---------------------------------------------------------------------#
        "anchors_path": 'yolo_anchors.txt',
        "anchors_mask": [[6, 7, 8], [3, 4, 5], [0, 1, 2]],
        # ---------------------------------------------------------------------#
        #   输入图片的大小，必须为32的倍数。
        # ---------------------------------------------------------------------#
        "input_shape": [640, 640],
        # ---------------------------------------------------------------------#
        #   只有得分大于置信度的预测框会被保留下来
        # ---------------------------------------------------------------------#
        "confidence": 0.5,
        # ---------------------------------------------------------------------#
        #   非极大抑制所用到的nms_iou大小
        # ---------------------------------------------------------------------#
        "nms_iou": 0.3,
        # ---------------------------------------------------------------------#
        #   该变量用于控制是否使用letterbox_image对输入图像进行不失真的resize，
        #   在多次测试后，发现关闭letterbox_image直接resize的效果更好
        # ---------------------------------------------------------------------#
        "letterbox_image": True
    }

    @classmethod
    def get_defaults(cls, n):
        if n in cls._defaults:
            return cls._defaults[n]
        else:
            return "Unrecognized attribute name '" + n + "'"

    # ---------------------------------------------------#
    #   初始化YOLO
    # ---------------------------------------------------#
    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults)
        for name, value in kwargs.items():
            setattr(self, name, value)
            self._defaults[name] = value

        import onnxruntime
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

        show_config(**self._defaults)

    def get_classes(self, classes_path):
        with open(classes_path, encoding='utf-8') as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names, len(class_names)

    def get_anchors(self, anchors_path):
        '''loads the anchors from a file'''
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

        print("success")

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

        feature_map_shape = [[int(j / (2 ** (i + 3))) for j in self.input_shape] for i in
                             range(len(self.anchors_mask))][::-1]
        for i in range(len(self.anchors_mask)):
            outputs[i] = np.reshape(outputs[i], (
            1, len(self.anchors_mask[i]) * (5 + self.num_classes), feature_map_shape[i][0], feature_map_shape[i][1]))

        outputs = self.bbox_util.decode_box(outputs)
        # ---------------------------------------------------------#
        #   将预测框进行堆叠，然后进行非极大抑制
        # ---------------------------------------------------------#
        results = self.bbox_util.non_max_suppression(np.concatenate(outputs, 1), self.num_classes, self.input_shape,
                                                     image_shape, self.letterbox_image, conf_thres=self.confidence,
                                                     nms_thres=self.nms_iou)

        if results[0] is None:
            return image

        top_label = np.array(results[0][:, 6], dtype='int32')
        top_conf = results[0][:, 4] * results[0][:, 5]
        top_boxes = results[0][:, :4]

        # ---------------------------------------------------------#
        #   设置字体与边框厚度
        # ---------------------------------------------------------#
        font = ImageFont.truetype(font='model_data/simhei.ttf',
                                  size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
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


def onnx_predict(img_name=None,
                 name_classes=None, name_classes_gbk=None,
                 file_name=None, location=None, people=None, pipe_number=None, comment=None,
                 dir_save_path=None, result_txt=None, conn=None):
    logging.info("load image")

    image_full_path = os.path.join(current_dir, str(img_name))

    image = Image.open(image_full_path)
    img_name_single = img_name.rsplit("/", 1)[-1]

    # 2023.8.11 修改返回值，包括图片、分数、类别
    r_image, out_scores, out_classes = yolo.detect_image(image)

    #  这张图要有检测结果才进入该循环
    if out_scores.size != 0:

        # 2023.3.3 只保存有预测结果的图片（只有background不算作有预测结果）
        # 存放预测结果的文件夹
        result_txt.write(img_name)
        result_txt.write("\r")
        result_txt.write("  识别出的种类有： ")
        result_txt.write("\r")

        # 2023.6.29 【新要求】补充 ----------数据库读写模块
        # 插入数据库中检测结果的字符串
        insert_detect_result = ""
        cursor = conn.cursor()

        # 如果不存在名为file_name的表，则创建新表
        # 因为数据库表名通常不支持点号，所以将.替换为_
        if not table_exists(table_name=file_name.replace(".", "_"), db_file_path=db_file_path):
            create_table_sql = '''
                CREATE TABLE {} (
                    时间 DATETIME,
                    地点 VARCHAR(50),
                    检测人 VARCHAR(50),
                    软管序号 VARCHAR(50),
                    图片名 VARCHAR(50),
                    检测结果 VARCHAR(50),
                    备注 VARCHAR(50)
                )
            '''.format(file_name.replace(".", "_"))
            cursor.execute(create_table_sql)
            logging.info("创建完成！")
        if table_exists(table_name=file_name.replace(".", "_"), db_file_path=db_file_path):
            logging.info("已有表！")

        for i in range(out_classes.shape[0]):
            if (out_classes[i] > 0) :
                temp = out_classes[i]
                logging.info("识别出：{}--{}".format(temp, name_classes_gbk[temp]))
                result_txt.write("  " + str(name_classes_gbk[temp]) + "   \t")
                result_txt.write("  " + str(np.round(out_scores[i], 4)) + "   \t")
                result_txt.write("\r")
                insert_detect_result = insert_detect_result + " " + \
                                       str(name_classes_gbk[temp])

        # 2023.6.29 【新要求】插入数据到数据库表中
        # 格式示例： 时间 图片名 检测结果
        insert_data_sql = '''
            INSERT INTO {} VALUES (?, ?, ?, ?, ?, ?, ?)
        '''.format(file_name.replace(".", "_"))
        values = (datetime.now(), location, people,
                  pipe_number, img_name, insert_detect_result,
                  comment)
        cursor.execute(insert_data_sql, values)

        conn.commit()
        # 关闭连接
        cursor.close()
        logging.info("成功写入数据 [名称:{}] [检测结果:{}] 到数据库的表 [{}] 中！"
                     .format(img_name, insert_detect_result, file_name.replace(".", "_")))

        r_image.save(str(os.path.join(dir_save_path, img_name_single)), quality=95, subsampling=0)
        result_txt.write("\r")

    logging.info("success!")
    return 1


def predict_main(onnx_=None, mode=None,
                 name_classes=None, name_classes_gbk=None,
                 location=None, people=None, pipe_number=None, comment=None,
                 timeF=None, filename=None):

    # 连接数据库
    conn_str = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + str(db_file_path)
    logging.info("成功创建并打开数据库，路径为{}".format(db_file_path))
    conn = pyodbc.connect(conn_str)

    # 图片检测
    if mode == 0:
        try:
            logging.info('success read image: ' + str(filename))
            file_rootname, _ = os.path.splitext(filename)
        except Exception as e:
            raise Exception(e)
        dir_save_path = str(file_rootname) + "_img_out/"
        if not os.path.exists(dir_save_path):
            os.makedirs(dir_save_path)
        f1 = open(os.path.join(dir_save_path, str(file_rootname) + '_predict_result.txt'), 'w', encoding='gbk')

        logging.info("start image predict")

        # 检测的主程序
        onnx_predict(img_name=filename,
                     name_classes=name_classes, name_classes_gbk=name_classes_gbk,
                     location=location, people=people, pipe_number=pipe_number, comment=comment,
                     file_name=filename, dir_save_path=dir_save_path, result_txt=f1,
                     conn=conn)

        f1.close()
        conn.close()
        logging.info("success, predict done!")
        logging.info("\n")

    # 视频检测
    if mode == 1:
        try:
            logging.info('success read video ' + str(filename))
            file_rootname, _ = os.path.splitext(filename)
        except Exception as e:
            raise Exception(e)
        output_dir = str(file_rootname) + '_img/'  # 保存图片文件夹路径
        output_img_type = '.jpg'  # 保存图片的格式
        vc = cv2.VideoCapture(filename)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        if vc.isOpened():
            rval, frame = vc.read()
        else:
            raise Exception('Video do not exist.')
        c = 1  # 统计帧数
        while rval:  # 循环读取视频帧
            rval, frame = vc.read()
            if not rval:
                break
            if c % int(timeF) == 0:  # 每隔timeF帧进行存储
                cv2.imwrite(output_dir + str(c) + output_img_type, frame)
                logging.info('success read frame No.' + str(c))
            c = c + 1
            cv2.waitKey(1)
        vc.release()
        # ------------------对img_out文件中图片批量预测
        logging.info("start video predict")
        dir_save_path = str(file_rootname) + "_img_out/"
        if not os.path.exists(dir_save_path):
            os.makedirs(dir_save_path)
        img_names = os.listdir(output_dir)
        img_names.sort(key=lambda x: int(x.split('.')[0]))  # 按照1，2，3 顺序读图片
        f1 = open(os.path.join(dir_save_path, str(file_rootname) + '_predict_result.txt'), 'a', encoding='gbk')
        for img_name in tqdm(img_names):

            img_name_path = os.path.join(output_dir, img_name)
            # 检测的主程序
            onnx_predict(img_name=img_name_path,
                         name_classes=name_classes, name_classes_gbk=name_classes_gbk,
                         location=location, people=people, pipe_number=pipe_number, comment=comment,
                         file_name=filename, dir_save_path=dir_save_path, result_txt=f1,
                         conn=conn)

        f1.close()
        conn.close()
        logging.info("success, all predict done!")


if __name__ == "__main__":
    # 输入配置参数
    _mode, _timeF, _filename, _location, _people, _pipe_number, _comment = load_arg()

    # 读取标签文件
    _name_classes, _name_classes_gbk = read_txt_lines(_classes_txt=_classes_txt,
                                                      _classes_gbk_txt=_classes_gbk_txt)

    yolo = YOLO_ONNX()

    # 进入预测 单张图片/视频
    predict_main(onnx_=yolo, mode=int(_mode),
                 name_classes=_name_classes,
                 name_classes_gbk=_name_classes_gbk,
                 location=_location, people=_people, pipe_number=_pipe_number, comment=_comment,
                 timeF=_timeF, filename=_filename)
