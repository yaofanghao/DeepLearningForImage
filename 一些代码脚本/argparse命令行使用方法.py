"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/4/26 9:57
    @Filename: cmd_test.py
    @Software: PyCharm     
"""
import argparse

parser = argparse.ArgumentParser(description='Test for argparse')
parser.add_argument('--mode', '-m', type=int,
                    help='mode 0或1 0为单张图片预测 1为视频预测 默认为1',
                    default=1)   # required=True,
parser.add_argument('--use_gpu', '-u', type=bool,
                    help='use_gpu 是否使用GPU环境 默认为True',
                    default=True)
parser.add_argument('--timeF', '-t', type=int,
                    help='timeF 视频帧计数间隔频率 默认为10',
                    default=10)
args = parser.parse_args()

if __name__ == "__main__":

    try:
        print("mode:{} \t use_gpu:{} \t tiemF:{} ".format(args.mode, args.use_gpu, args.timeF))
    except Exception as e:
        print(e)
