"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/6/29 9:51
    @Filename: 测试-数据库读写.py
    @Software: PyCharm     
"""
import os, pyodbc
from datetime import datetime

# 检测表名是否已存在的函数
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


def create_insert_table(db_file_path, table_name, name, detect_result):

    conn_str = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + db_file_path
    print("成功创建并打开数据库，路径为{}".format(db_file_path))

    conn = pyodbc.connect(conn_str)

    # 创建游标
    cursor = conn.cursor()

    # 删除表
    # delete_table_sql = '''
    #     DROP TABLE {};
    # '''.format(table_name)
    # cursor.execute(delete_table_sql)

    # 执行一个简单的查询语句
    # query = 'SELECT COUNT(*) FROM {}'.format("示例1")
    # cursor.execute(query)
    #
    # # 获取结果
    # result = cursor.fetchone()
    # if result:
    #     row_count = result[0]
    #     print("数据库连接成功，行数为：", row_count)
    # else:
    #     print("数据库连接失败，请检查连接配置和数据库文件路径")

    # 如果不存在表，则创建新表
    if not table_exists(table_name, db_file_path=db_file_path):
        create_table_sql = '''
            CREATE TABLE {} (
                时间 DATETIME,
                名称 VARCHAR(50),
                检测结果 VARCHAR(50)
            )  
        '''.format(table_name)
        cursor.execute(create_table_sql)
        print("创建完成！")
    if table_exists(table_name, db_file_path=db_file_path):
        print("已有表！")

    # 插入数据到表中
    insert_data_sql = '''
    INSERT INTO {} VALUES (?, ?, ?)
    '''.format(table_name)

    values = (datetime.now(), name, detect_result)
    cursor.execute(insert_data_sql, values)

    # 提交事务
    conn.commit()
    # 关闭连接
    cursor.close()
    conn.close()
    print("成功写入数据 [名称:{}] [检测结果:{}] 到数据库的 [表:{}] 中！"
          .format(name, detect_result, table_name))
    print("程序结束！")

if __name__ == "__main__":

    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 构造数据库文件，并连接到Access数据库，DBQ需要是绝对路径
    db_file_path = os.path.join(current_dir, 'predict_result.accdb')

    table_name = "示例1"
    name = 'test22.jpg'
    detect_result = '11 22 擦伤 鼓波 多余物'
    create_insert_table(db_file_path=db_file_path, table_name=table_name,
                        name=name, detect_result=detect_result)