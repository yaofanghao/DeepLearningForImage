# 项目-基于PyQt的人工智能诊断系统软件设计

* 2023.10.21- 软件系统重构，计划分为肠化诊断和OLGIM评估两个模块
* 2023.10.21 实现OLGIM综合评估模型界面
* 2023.10.23- 实现肠化亚型识别界面

## 存在的一些bug-- 待修复
* 导出诊断报告pdf界面美化


## 开发环境：
* PyCharm Community Edition 2023.1
* python 3.8.0
* PyQt 5.15.9
* tensorflow-gpu 2.8.0
* Pillow 9.5.0
* h5py 3.8.0
* keras 2.8.0
* numpy 1.24.4
* opencv-python 4.7.0.72
* tqdm 4.65.0
* reportlab 4.0.6

# 设计逻辑
## main.py 主函数
**ui可以生成py，但py无法转换为ui！**
**注意！ui只负责修改显示样式。逻辑实现均在main.py中修改！**
* 实现各界面之间的跳转、交流

## InitWidget.py 
初始诊断系统选择界面

## InfoWidget.py
病人基本信息界面

## ChanghuaWidget.py
肠化亚型识别界面

## OLGIMWidget.py
OLGIM综合评估模型界面

## apprcc.qrc
存放图片等资源文件链接

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
* 保存图片参考自 https://blog.csdn.net/m0_47682721/article/details/123928585
* 进度条对话框参考自 https://blog.csdn.net/yurensan/article/details/121025642
* 打开文件夹并读取文件列表参考自 https://blog.csdn.net/weixin_45875105/article/details/113185870
* 多窗口数据传递参考自 https://blog.csdn.net/jdl1206/article/details/121619463
* pyinstaller打包和spec配置参考自 https://blog.csdn.net/qq_38856833/article/details/115287480?spm=1001.2101.3001.6650.10&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-10-115287480-blog-93868769.pc_relevant_multi_platform_whitelistv3&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-10-115287480-blog-93868769.pc_relevant_multi_platform_whitelistv3&utm_relevant_index=12
