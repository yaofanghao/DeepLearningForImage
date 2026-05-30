"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/11/8 14:34
    @Filename: my_onnx_save_to_dataset.py
    @Software: PyCharm     
"""

import os
import pyodbc
from datetime import datetime
import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


# #########################参数设置区域
argparse_txt = "argparse.txt"  # 配置参数文件
current_dir = os.path.dirname(os.path.abspath(__file__))
db_file_path = os.path.join(current_dir, 'predict_result.mdb')  # 构造数据库文件，并连接到Access数据库，DBQ需要是绝对路径
table_name = "result"

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


def save_to_database():
    # print("1+1")

    f_arg = open(os.path.join(current_dir, "argparse.txt"), "r")
    lines_arg = f_arg.read().splitlines()
    logging.info("success load arg from: {}".format(argparse_txt))
    logging.info("setting mode: {} \t  timeF:{} "
                 .format(lines_arg[0], lines_arg[1]))
    logging.info("success read filename: {} \t".format(lines_arg[2]))

    _mode, _timeF, _filename, _location, _people, _pipe_number, _pici_number, _comment =     \
        lines_arg[0], lines_arg[1], lines_arg[2], \
        lines_arg[3], lines_arg[4], \
        lines_arg[5], lines_arg[6], lines_arg[7]

    # 不带后缀的图片名
    _filename_name, _ = os.path.splitext(_filename)
    output_path = current_dir + "\\" + _filename_name + "_img_out\\"
    print(output_path)

    # # 连接数据库
    conn_str = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + str(db_file_path)
    logging.info("成功创建并打开数据库，路径为{}".format(db_file_path))
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    if not table_exists(table_name=table_name, db_file_path=db_file_path):
        create_table_sql = '''
            CREATE TABLE {} (
                时间 VARCHAR(50),
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

    result_txt = str(output_path + _filename_name + '_predict_result.txt')

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
                  _pipe_number, _pici_number, img_name_single, insert_detect_result,
                  _comment)
        cursor.execute(insert_data_sql, values)
    conn.commit()

    #   关闭数据库连接
    cursor.close()

    return 1

if __name__ == "__main__":
    save_to_database()