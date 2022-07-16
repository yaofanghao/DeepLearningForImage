# 项目-基于PyQt的人工智能诊断系统软件设计

开发时间：
* 2022.7.14-

开发环境：
* PyCharm Community Edition 2020.3.2 @yaofanghao
* Python 3.8.13
* PyQt 5.15.4
* Tensorflow 2.7.0
* pillow 9.0.1
* h5py 3.7.0
* keras 2.7.0
* numpy 1.23.1
* opencv-python 4.5.4.60
* tqdm 4.64.0

# 设计逻辑
## main.py 主函数
**ui可以生成py，但py无法转换为ui！**
**注意！ui只负责修改显示样式。逻辑实现均在main.py中修改！**
* 实现各界面之间的跳转、交流

## InitWidget.py 
初始诊断系统选择界面

## InfoWidget.py
病人基本信息界面

## AiqianWidget.py 
癌前病变诊断界面

## EGCWidget.py
早癌EGC诊断系统界面

## EGC_yolo_predict 文件夹
内含EGC预测模型yolov3的模型、权重

## apprcc.qrc
存放图片等资源文件链接

------
## 实现功能
已完成：
* 按钮实现各界面之间的切换 -7.15完成

未完成：
* 填写病人信息生成word 
* 读取指定文件夹图片功能
    * 选择单张图片预测
    * 选择文件夹图片批量预测
* 显示预测后的图片
* 保存预测后的图片
* 医生填写的诊断结果生成报告保存至word
* 界面美化、字体、背景图 
* 其他功能和细节待补充
  
------
# 参考资料
* **pyqt5快速开发与实战--王硕**
* pyqt5实战指南-手把手教你掌握100个精彩案例--白振勇
* C++GUI Qt4编程--布兰切特
* Qt5.9 C++开发指南--王维波
* qt官网 https://www.qt.io/cn/
* pyqt官网 https://www.riverbankcomputing.com/
* pyqt入门教程 https://blog.csdn.net/m0_57021623/article/details/123459038
* 界面切换参考自 https://blog.csdn.net/weixin_43734095/article/details/106783108
* 背景图片设置参考自 https://blog.csdn.net/qq_38161040/article/details/88363916
* 样式表参考自 https://blog.csdn.net/zhouyingge1104/article/details/95377946
* 保存图片参考自 http://t.csdn.cn/S4cR
