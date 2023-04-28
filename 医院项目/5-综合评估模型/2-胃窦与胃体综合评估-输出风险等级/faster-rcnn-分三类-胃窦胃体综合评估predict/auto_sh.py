"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/4/28 10:06
    @Filename: auto_sh.py.py
    @Software: PyCharm     
"""

# 自动化脚本
# 使用方法示例
#     终端输入 python auto_sh.py img
# 对img文件夹中的多个病人的多种病例图
# 调用 predict_mix.py 进行批量预测
import os
import sys
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # 忽略TensorFlow的warning信息
from tqdm import tqdm


def length_of_dir(dir_name):
    files = os.listdir(dir_name)
    return len(files)


# def collect_txt(dir_origin):
#     # 使用bat命令  type *.txt >> collection.txt
#     collect_cmd = "cd " + str(dir_origin) + " && collection_txt.bat"
#     os.system(collect_cmd)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("example: python auto_sh.py img")
        dir_origin = "img"  # 输入待预测的总的图片文件夹名称 不带斜杠
    else:  # 手动传入待预测文件夹名称
        dir_origin = sys.argv[1]
        print("start: python auto_sh.py {}".format(dir_origin))

    length_of_img_dir = length_of_dir(str(dir_origin))

    name_dir = os.listdir(dir_origin)
    for _name in tqdm(name_dir):
        print("start predict for {}".format(_name))
        cmd = "python predict_mix.py " + str(_name)
        os.system(cmd)
    print("success! all done!")

    # 合并所有预测结果的txt 目前未成功
    # 目前可用方法：直接去文件夹下使用bat即可
    # collect_txt(dir_origin)
