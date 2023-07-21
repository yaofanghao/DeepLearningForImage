"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/7/13 11:04
    @Filename: my_onnx_test.py
    @Software: PyCharm     
"""

# 2023.7.20-补充 mode=2时 摄像头读取功能

import os, sys
from tqdm import tqdm
import onnx
import onnxruntime as ort
import numpy as np
import cv2
import copy
from PIL import Image, ImageFont, ImageDraw
import pyodbc
from datetime import datetime
import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


# #########################参数设置区域
_classes_txt = "class_name.txt"  # 分类标签文件
_classes_gbk_txt = "class_name_gbk.txt"  # 分类标签文件中文版
argparse_txt = "argparse.txt"  # 配置参数文件
current_dir = os.path.dirname(os.path.abspath(__file__))
db_file_path = os.path.join(current_dir, 'predict_result.mdb')  # 构造数据库文件，并连接到Access数据库，DBQ需要是绝对路径

image_size = 480  # 图像尺寸
num_classes = 9  # 分类类别 八类+背景一类
area_threshold = 0  # 最小面积阈值

def load_arg():
    # 方法二 以读取配置文件argparse.txt的方式载入参数
    # 配置参数说明：
    # 第一项为预测模式 0或1 0为单张图片预测 1为视频预测 默认为1
    # 第二项为视频帧计数间隔频率 影响视频检测速率，可任意设置，建议值10-30之间
    # 第三项为待检测图片\视频的相对路径

    f_arg = open(argparse_txt, "r", encoding='gbk')
    lines_arg = f_arg.read().splitlines()
    logging.info("success load arg from: {}".format(argparse_txt))
    logging.info("setting mode: {} \t  timeF:{} "
                 .format(lines_arg[0], lines_arg[1]))
    logging.info("success read filename: {} \t".format(lines_arg[2]))
    return lines_arg[0], lines_arg[1], lines_arg[2]


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


# 2023.7.17
# onnxruntime 自定义类
class OnnxProcess():
    def __init__(self, **kwargs):
        self.onnx_model_name = "hrnet-pytorch.onnx"
        self.model = onnx.load(self.onnx_model_name)
        self.sess = ort.InferenceSession(self.model.SerializeToString())

def load(onnx_model_name):
    logging.info("load onnx")
    # 创建ONNX运行时
    onnx_ = OnnxProcess()
    onnx_.onnx_model_name = "hrnet-pytorch.onnx"
    onnx_.model = onnx.load(onnx_model_name)
    onnx_.sess = ort.InferenceSession(onnx_.model.SerializeToString())

    return onnx_


def onnx_predict(img_name=None, onnx_=None,
                 name_classes=None, name_classes_gbk=None,
                 file_name=None, dir_save_path=None, result_txt=None,
                 conn=None):
    logging.info("load image")

    # 加载并预处理输入图像
    image = cv2.imread(img_name)
    old_img = copy.deepcopy(image)
    orininal_h = np.array(image).shape[0]
    orininal_w = np.array(image).shape[1]

    image = cv2.resize(image, (image_size, image_size))
    image = image.astype(np.float32) / 255.0  # 归一化到[0, 1]范围
    image = np.transpose(image, (2, 0, 1))
    image = np.expand_dims(image, axis=0)  # 添加批次维度

    # 执行推理
    logging.info("start predict")
    # input_name = sess.get_inputs()[0].name
    # output_name = sess.get_outputs()[0].name
    input_name = 'images'
    output_name = 'output'
    output = onnx_.sess.run([output_name], {input_name: image})[0]

    # 后处理输出
    output = np.squeeze(output)  # 去除批次维度
    output = np.argmax(output, axis=0)  # 获取每个像素的类别索引

    # 将输出可视化
    class_colors = [(0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128),
                       (0, 128, 128), (128, 128, 128), (64, 0, 0)]  # 类别颜色映射表
    # class_colors = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
    #                    (0, 0, 0), (0, 0, 0), (64, 0, 0)]  # 类别颜色映射表

    result = np.zeros((image_size, image_size, 3), dtype=np.uint8)
    for i in range(image_size):
        for j in range(image_size):
            result[i, j] = class_colors[output[i, j]]
    result = cv2.resize(result, (orininal_w, orininal_h), interpolation=cv2.INTER_LINEAR)

    # 图像叠加
    alpha = 0.4  # 第一张图像的权重
    beta = 0.8  # 第二张图像的权重
    mix = cv2.addWeighted(old_img, alpha, result, beta, 0)

    # 在图像上绘制文字
    # 将图像从OpenCV格式转换为PIL格式
    image_pil = Image.fromarray(cv2.cvtColor(mix, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(image_pil)
    font = ImageFont.truetype(font='simhei.ttf',size=30)  # 修改字体大小
    color = 'red'
    output_class_name = np.array([], dtype=int)  # 存放预测类别结果的数组
    step = 1  # 在图上绘制预测类别的显示间隔
    draw.text((70, 30 * step), '【检测结果】', font=font, fill=color)

    for i in range(1, num_classes):
        num = np.count_nonzero((result == class_colors[i]).all(axis=2))
        if (num > area_threshold) & (name_classes is not None):
            step = step + 1
            draw.text((70, 30 * step), str(name_classes_gbk[i]), font=font, fill=color)
            output_class_name = np.append(output_class_name, i)
    # 将图像从PIL格式转换回OpenCV格式
    mix = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

    #  这张图要有检测结果才进入该循环
    if output_class_name.size > 0:
        max_output_class_name = np.max(output_class_name)
        img_name_single = img_name.rsplit("/",1)[-1]

        # 2023.3.3 只保存有预测结果的图片（只有background不算作有预测结果）
        # 代码原理：最大预测结果类别大于0，说明预测出的不是只有background，此时保存图片
        if max_output_class_name > 0:
            logging.info("\n")
            logging.info("{}-发现缺陷--{}".format(img_name, output_class_name))
            # 存放预测结果的文件夹
            result_txt.write(img_name)
            result_txt.write("\r")
            result_txt.write("  识别出的种类有： ")

            # 2023.6.29 【新要求】补充 ----------数据库读写模块
            # 插入数据库中检测结果的字符串
            insert_detect_result = ""

            # # 连接数据库
            # conn_str = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + str(db_file_path)
            # logging.info("成功创建并打开数据库，路径为{}".format(db_file_path))
            # conn = pyodbc.connect(conn_str)
            # 创建游标
            cursor = conn.cursor()

            # 如果不存在名为file_name的表，则创建新表
            # 因为数据库表名通常不支持点号，所以将.替换为_
            if not table_exists(table_name=file_name.replace(".", "_"), db_file_path=db_file_path):
                create_table_sql = '''
                    CREATE TABLE {} (
                        时间 DATETIME,
                        图片名 VARCHAR(50),
                        检测结果 VARCHAR(50)
                    )
                '''.format(file_name.replace(".", "_"))
                cursor.execute(create_table_sql)
                logging.info("创建完成！")
            if table_exists(table_name=file_name.replace(".", "_"), db_file_path=db_file_path):
                logging.info("已有表！")

            for i in range(output_class_name.shape[0]):
                if (output_class_name[i] > 0) :
                    temp = output_class_name[i]
                    logging.info("识别出：{}--{}".format(temp, name_classes_gbk[temp]))
                    result_txt.write("    " + str(name_classes_gbk[temp]) + "\t")
                    insert_detect_result = insert_detect_result + " " + \
                                           str(name_classes_gbk[temp])

                # 2023.6.3 补充焊接缺陷的判定
                if output_class_name[i] == 8:
                    result_txt.write("\n  识别出焊接缺陷！程序立即停止！")
                    cv2.imwrite(str(os.path.join(dir_save_path, img_name_single)), mix)
                    insert_detect_result = insert_detect_result + " " + str(name_classes_gbk[8])

                    # 焊接缺陷写入数据库的代码单独列出：
                    insert_data_sql = '''
                        INSERT INTO {} VALUES (?, ?, ?)
                    '''.format(file_name.replace(".", "_"))
                    values = (datetime.now(), img_name, insert_detect_result)
                    cursor.execute(insert_data_sql, values)
                    conn.commit()
                    cursor.close()
                    conn.close()
                    logging.info("成功写入数据 [名称:{}] [检测结果:{}] 到数据库的表 [{}] 中！"
                                 .format(img_name, insert_detect_result, file_name.replace(".", "_")))
                    logging.error("识别出焊接缺陷！程序立即停止！")
                    sys.exit(1)  # 异常退出，程序立即终止

            result_txt.write("\r")
            result_txt.write("  预测概率值最高的类别为： " + name_classes_gbk[max_output_class_name])

            # 2023.6.29 【新要求】插入数据到数据库表中
            # 格式示例： 时间 图片名 检测结果
            insert_data_sql = '''
                INSERT INTO {} VALUES (?, ?, ?)
            '''.format(file_name.replace(".", "_"))
            values = (datetime.now(), img_name, insert_detect_result)
            cursor.execute(insert_data_sql, values)

            conn.commit()
            # 关闭连接
            cursor.close()
            # conn.close()
            logging.info("成功写入数据 [名称:{}] [检测结果:{}] 到数据库的表 [{}] 中！"
                         .format(img_name, insert_detect_result, file_name.replace(".", "_")))

        cv2.imwrite(str(os.path.join(dir_save_path, img_name_single)), mix)
        result_txt.write("\r")

    logging.info("success!")
    # cv2.imshow('Mix Result', mix)
    # cv2.imshow('Segmentation Result', result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return 1


def onnx_predict_camera(image=None, onnx_=None,
                 name_classes=None, name_classes_gbk=None,
                 dir_save_path=None, result_txt=None,
                 flag=None, conn=None):
    logging.info("load image")

    img_name_single = str(flag) + ".jpg"
    table_name = "camera"

    # 加载并预处理输入图像
    old_img = copy.deepcopy(image)
    orininal_h = np.array(image).shape[0]
    orininal_w = np.array(image).shape[1]

    image = cv2.resize(image, (image_size, image_size))
    image = image.astype(np.float32) / 255.0  # 归一化到[0, 1]范围
    image = np.transpose(image, (2, 0, 1))
    image = np.expand_dims(image, axis=0)  # 添加批次维度

    # 执行推理
    logging.info("start predict")
    # input_name = sess.get_inputs()[0].name
    # output_name = sess.get_outputs()[0].name
    input_name = 'images'
    output_name = 'output'
    output = onnx_.sess.run([output_name], {input_name: image})[0]

    # 后处理输出
    output = np.squeeze(output)  # 去除批次维度
    output = np.argmax(output, axis=0)  # 获取每个像素的类别索引

    # 将输出可视化
    class_colors = [(0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128),
                       (0, 128, 128), (128, 128, 128), (64, 0, 0)]  # 类别颜色映射表

    result = np.zeros((image_size, image_size, 3), dtype=np.uint8)
    for i in range(image_size):
        for j in range(image_size):
            result[i, j] = class_colors[output[i, j]]
    result = cv2.resize(result, (orininal_w, orininal_h), interpolation=cv2.INTER_LINEAR)

    # 图像叠加
    alpha = 0.4  # 第一张图像的权重
    beta = 0.8  # 第二张图像的权重
    mix = cv2.addWeighted(old_img, alpha, result, beta, 0)

    # 在图像上绘制文字
    # 将图像从OpenCV格式转换为PIL格式
    image_pil = Image.fromarray(cv2.cvtColor(mix, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(image_pil)
    font = ImageFont.truetype(font='simhei.ttf',size=30)  # 修改字体大小
    color = 'red'
    output_class_name = np.array([], dtype=int)  # 存放预测类别结果的数组
    step = 1  # 在图上绘制预测类别的显示间隔
    draw.text((70, 30 * step), '【检测结果】', font=font, fill=color)

    for i in range(1, num_classes):
        num = np.count_nonzero((result == class_colors[i]).all(axis=2))
        if (num > area_threshold) & (name_classes is not None):
            step = step + 1
            draw.text((70, 30 * step), str(name_classes_gbk[i]), font=font, fill=color)
            output_class_name = np.append(output_class_name, i)
    # 将图像从PIL格式转换回OpenCV格式
    mix = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

    #  这张图要有检测结果才进入该循环
    if output_class_name.size > 0:
        max_output_class_name = np.max(output_class_name)

        # 2023.3.3 只保存有预测结果的图片（只有background不算作有预测结果）
        # 代码原理：最大预测结果类别大于0，说明预测出的不是只有background，此时保存图片
        if max_output_class_name > 0:
            logging.info("\n")
            logging.info("视频检测-发现缺陷--{}".format(output_class_name))
            # 存放预测结果的文件夹
            result_txt.write("视频检测")
            result_txt.write("\r")
            result_txt.write("  识别出的种类有： ")

            # 2023.6.29 【新要求】补充 ----------数据库读写模块
            # 插入数据库中检测结果的字符串
            insert_detect_result = ""

            # # 连接数据库
            # conn_str = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + str(db_file_path)
            # logging.info("成功创建并打开数据库，路径为{}".format(db_file_path))
            # conn = pyodbc.connect(conn_str)
            # 创建游标
            cursor = conn.cursor()

            # 如果不存在名为file_name的表，则创建新表
            # 因为数据库表名通常不支持点号，所以将.替换为_
            if not table_exists(table_name=table_name, db_file_path=db_file_path):
                create_table_sql = '''
                    CREATE TABLE {} (
                        时间 DATETIME,
                        图片名 VARCHAR(50),
                        检测结果 VARCHAR(50)
                    )
                '''.format(table_name)
                cursor.execute(create_table_sql)
                logging.info("创建完成！")
            if table_exists(table_name=table_name, db_file_path=db_file_path):
                logging.info("已有表！")

            for i in range(output_class_name.shape[0]):
                if (output_class_name[i] > 0) :
                    temp = output_class_name[i]
                    logging.info("识别出：{}--{}".format(temp, name_classes_gbk[temp]))
                    result_txt.write("    " + str(name_classes_gbk[temp]) + "\t")
                    insert_detect_result = insert_detect_result + " " + \
                                           str(name_classes_gbk[temp])

                # 2023.6.3 补充焊接缺陷的判定
                if output_class_name[i] == 8:
                    result_txt.write("\n  识别出焊接缺陷！程序立即停止！")
                    cv2.imwrite(str(os.path.join(dir_save_path, img_name_single)), mix)
                    insert_detect_result = insert_detect_result + " " + str(name_classes_gbk[8])

                    # 焊接缺陷写入数据库的代码单独列出：
                    insert_data_sql = '''
                        INSERT INTO {} VALUES (?, ?, ?)
                    '''.format(table_name)
                    values = (datetime.now(), img_name_single, insert_detect_result)
                    cursor.execute(insert_data_sql, values)
                    conn.commit()
                    cursor.close()
                    conn.close()
                    logging.info("成功写入数据 [名称:{}] [检测结果:{}] 到数据库的表 [{}] 中！"
                                 .format(img_name_single, insert_detect_result, table_name))
                    logging.error("识别出焊接缺陷！程序立即停止！")
                    sys.exit(1)  # 异常退出，程序立即终止

            result_txt.write("\r")
            result_txt.write("  预测概率值最高的类别为： " + name_classes_gbk[max_output_class_name])

            # 2023.6.29 【新要求】插入数据到数据库表中
            # 格式示例： 时间 图片名 检测结果
            insert_data_sql = '''
                INSERT INTO {} VALUES (?, ?, ?)
            '''.format(table_name)
            values = (datetime.now(), img_name_single, insert_detect_result)
            cursor.execute(insert_data_sql, values)

            conn.commit()
            # 关闭连接
            cursor.close()
            # conn.close()
            logging.info("成功写入数据 [名称:{}] [检测结果:{}] 到数据库的表 [{}] 中！"
                         .format(img_name_single, insert_detect_result, table_name))

        cv2.imwrite(str(os.path.join(dir_save_path, img_name_single)), mix)
        result_txt.write("\r")

    logging.info("success!")
    # cv2.imshow('Mix Result', mix)
    # cv2.imshow('Segmentation Result', result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return 1


def predict_main(onnx_=None, mode=None,
                 name_classes=None, name_classes_gbk=None,
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
        onnx_predict(img_name=filename, onnx_=onnx_,
                     name_classes=name_classes, name_classes_gbk=name_classes_gbk,
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
            onnx_predict(img_name=img_name_path, onnx_=onnx_,
                         name_classes=name_classes, name_classes_gbk=name_classes_gbk,
                         file_name=filename, dir_save_path=dir_save_path, result_txt=f1,
                         conn=conn)

        f1.close()
        conn.close()
        logging.info("success, all predict done!")

    # 摄像头检测
    if mode == 2:
        dir_save_path = "camera_img_out/"
        if not os.path.exists(dir_save_path):
            os.makedirs(dir_save_path)
        f1 = open(os.path.join(dir_save_path, 'camera_predict_result.txt'), 'w', encoding='gbk')

        flag = 0
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 每隔timeF检测一次
            if flag % int(timeF) == 0:
                logging.info("start image predict, flag={}".format(flag))

                # 检测的主程序
                onnx_predict_camera(image=frame, onnx_=onnx_,
                             name_classes=name_classes, name_classes_gbk=name_classes_gbk,
                             dir_save_path=dir_save_path, result_txt=f1,
                             flag=flag, conn=conn)
            flag = flag+1

            cv2.imshow('detection result', frame)
            # logging.info("success, predict done!")
            # logging.info("\n")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                f1.close()
                conn.close()
                break


if __name__ == "__main__":
    # 输入配置参数
    _mode, _timeF, _filename = load_arg()

    # 读取标签文件
    _name_classes, _name_classes_gbk = read_txt_lines(_classes_txt=_classes_txt,
                                                      _classes_gbk_txt=_classes_gbk_txt)

    # 加载onnx模型
    onnx_model_name = "hrnet-pytorch.onnx"
    onnx_ = load(onnx_model_name=onnx_model_name)

    # 进入预测 单张图片/视频
    predict_main(onnx_=onnx_, mode=int(_mode),
                 name_classes=_name_classes,
                 name_classes_gbk=_name_classes_gbk,
                 timeF=_timeF, filename=_filename)
