"""

    -*- coding: utf-8 -*-
    @Author  : yaofanghao
    @Last edit time    : 2023/4/18 11:18
    @File    : auto_sh.py
    @Software: PyCharm 
    
"""
# 传入参数： 待预测输入图片文件夹名称 不带斜杠
# 默认为 test 文件夹
# 示例：
#     如果要预测文件夹 dir1
#     则在终端输入： python auto_sh.py dir1
import os, sys
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # 忽略TensorFlow的warning信息

def length_of_dir(dir_name):
    files = os.listdir(dir_name)
    return len(files)

if __name__ == "__main__":
    if len(sys.argv) == 1:
       print("start: python auto_predict_3class.py test")
       dir_origin = "test"  # 输入图片文件夹名称 不带斜杠
    else:  # 手动传入待预测文件夹名称
       dir_origin = sys.argv[1]

    #  ##########  第一阶段 预测三分类模型  ###########
    print("start predict for 3 class...")
    cmd = "python auto_predict_3class.py " + str(dir_origin)
    os.system(cmd)

    #  ##########  第二阶段 预测二分类模型  ###########
    print("start predict for 2 class...")
    cmd = "python auto_predict_2class.py " + str(dir_origin)
    os.system(cmd)
    print("success!")

    #  ##########  第三阶段 统计预测结果  ###########
    print("caculate accuarcy of predict...")
    dir_origin_ = str("predict_result_") + str(dir_origin) + "/" + "img_out_"
    all_save_path_0 = str(dir_origin_) + "0-1/"
    all_save_path_2 = str(dir_origin_) + "2/"
    all_save_path_3 = str(dir_origin_) + "3/"
    all_save_path_none = str(dir_origin_) + "none/"

    num0 = length_of_dir(all_save_path_0)
    num2 = length_of_dir(all_save_path_2)
    num3 = length_of_dir(all_save_path_3)
    none = length_of_dir(all_save_path_none)

    rate_0_1 = (num0 / (num0+num2+num3+none)) * 100
    rate_2 = (num2 / (num0+num2+num3+none)) * 100
    rate_3 = (num3 / (num0+num2+num3+none)) * 100
    rate_none = (none / (num0 + num2 + num3 + none)) * 100
    print("识别为0-1分：", num0)
    print("识别为2分：", num2)
    print("识别为3分：", num3)
    print("无结果：", none)
    print("识别为0-1分的比例：", str(rate_0_1) + '%')
    print("识别为2分的比例：", str(rate_2) + '%')
    print("识别为3分的比例：", str(rate_3) + '%')
    print("无结果的比例：", str(rate_none) + '%')

    f_dir = str("predict_result_") + str(dir_origin) + "/"
    f = open(os.path.join(f_dir, 'predict_report.txt'), 'a')
    f.write("识别为0-1分：" + str(num0))
    f.write("\r")
    f.write("识别为2分：" + str(num2))
    f.write("\r")
    f.write("识别为3分：" + str(num3))
    f.write("\r")
    f.write("无结果：" + str(none))
    f.write("\r")
    f.write("识别为0分的比例：" + str(rate_0_1) + '%')
    f.write("\r")
    f.write("识别为2分的比例：" + str(rate_2) + '%')
    f.write("\r")
    f.write("识别为3分的比例：" + str(rate_3) + '%')
    f.write("\r")
    f.write("无结果的比例：" + str(rate_none) + '%')
    f.write("\r")
    f.close()
    print("all done!")

# ---------------------------------
    # 该方法也不正确 二阶段模型预测时遇到问题，全部 results 返回为0，未找到原因：
    # from auto_predict_3class import predict_3class
    # from auto_predict_2class import predict_2class
    # print("start predict for 3 class...")
    # predict_3class()
    #
    # print("start predict for 2 class...")
    # predict_2class()
    #
    # print("success!")

