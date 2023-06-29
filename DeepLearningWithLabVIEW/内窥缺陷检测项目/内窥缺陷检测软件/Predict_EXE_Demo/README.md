"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/4/25 10:42
    @Filename: READEM.md.py
    @Software: PyCharm     
"""
## 源码 predict_for_exe.py

* 配置文件
  ```python
  _classes_txt = "class_name.txt"  # 分类标签文件
  _classes_gbk_txt = "class_name_gbk.txt"  # 分类标签文件中文版
  argparse_txt = "argparse.txt"  # 配置参数文件
  ```
  * 分为单张图片/视频检测两种模式，针对视频逐帧分解视频到img文件夹中
  * 对img文件夹图片逐帧进行模型预测，只保存有预测结果的图片到img_out文件夹中
  * 预测结果同时导出至txt或其他形式的文本 
* 提高要求：
  * 优化程序结构，提升程序运行速度
  * 输出结果的地方和数据库相结合，labview后续可以调用数据库

## exe导出
* cmd下输入
  * pyinstaller -F -i ./fac.ico tree.py
  * pyinstaller -F -c main.py
    * -i./xxx.ico  是设置图标，选填
    * -F 打包为一个exe （-D不打包为一个exe，不推荐）
    * -c 带控制台，一般用于查找错误 （-w 不带控制台）