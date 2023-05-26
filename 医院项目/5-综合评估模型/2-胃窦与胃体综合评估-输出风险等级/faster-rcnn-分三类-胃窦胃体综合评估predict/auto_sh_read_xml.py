"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/4/28 10:06
    @Filename: auto_sh.py.py
    @Software: PyCharm     
"""

# 自动化脚本
# 使用方法示例
#     终端输入 python auto_sh_read_xml.py img

import os
import sys
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # 忽略TensorFlow的warning信息
from tqdm import tqdm

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("example: python auto_sh_read_xml.py img")
        dir_origin = "img"  # 输入待预测的总的图片文件夹名称 不带斜杠
    else:  # 手动传入待预测文件夹名称
        dir_origin = sys.argv[1]
        print("start: python auto_sh_read_xml.py {}".format(dir_origin))

    name_dir = os.listdir(dir_origin)
    for _name in tqdm(name_dir):
        print("start read_xml for {}".format(_name))
        cmd = "python read_xml.py " + str(_name)
        os.system(cmd)
    print("success! all done!")

