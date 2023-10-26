# 基于PyQt的人工智能诊断系统软件设计

* 2023.10.21- **软件系统重构**，旧版本已在2022.7实现，此版本根据需求重构
* 2023.10.21 实现OLGIM综合评估模型界面
* 2023.10.23-10.24 实现肠化亚型识别界面
* 2023.10.24 把各界面的类的代码模块化分离至ChanghuaUi_OLGIMUi.py和InitUi_InfoUi.py
* 2023.10.24 简化删除一些冗余代码
* 2023.10.26 修改美化界面样式

## 目前存在的一些bug和可优化内容
### 已修复：
* 图片传入detect_image出现数据溢出问题，th、tw、tx、ty值过大
  * 因为resnet.py中启用了leaky-relu和注意力机制，而这里所用的h5模型训练时没有加入这两个模块，因此出现模型结构不匹配和计算错误问题
* 已有预测结果的图片，不应该重复预测浪费时间
  * 预测图片时增加判断语句 
  ```python 
  if not os.path.exists(os.path.join('img_out_OLGIM/', img_name.replace(".jpg", ".png"))):
  ```
* 检测时增加进度条，显示“模型启动中”

### 待完成：
* **重大问题！OLGIM的模型权重预测不出结果**，未找到原因
* 肠化诊断界面中，点击“填写报告”和“返回诊断系统选择界面”无反应
* 填写报告单一栏中，增加返回按钮，可以回到诊断界面
* 导出诊断报告修改为保存成word格式
* 界面美化
* 软件运行加速

## 开发环境：
* PyCharm Community Edition 2023.1
* python 3.8.0
* PyQt 5.15.9
* tensorflow-gpu 2.8.0
* keras 2.8.0
* Pillow 9.5.0
* h5py 3.8.0
* keras 2.8.0
* numpy 1.24.4
* opencv-python 4.7.0.72
* tqdm 4.65.0
* reportlab 4.0.6

# 设计逻辑
## main.py 主函数
* 实现各界面之间的跳转、交流
* InitUi_InfoUi.py
* ChanghuaUi_OLGIMUi.py
  * 各界面的类的函数

## widgets 文件夹
* **ui可以生成py，但py无法转换为ui！**
* **注意！ui只负责修改显示样式。逻辑实现均在main.py中修改！**
* InitWidget.py 
  * 初始诊断系统选择界面
* InfoWidget.py
  * 病人基本信息界面
* ChanghuaWidget.py
  * 肠化亚型识别界面
* OLGIMWidget.py
  * OLGIM综合评估模型界面
* apprcc.qrc
  * 存放图片等资源文件链接

## nets 文件夹
* 模型网络代码
* 训练好的模型参数h5文件
* 类别标签文件txt文件

## utils 文件夹
* 模型网络代码

# 参考资料
* **pyqt5快速开发与实战--王硕**
* pyqt5实战指南-手把手教你掌握100个精彩案例--白振勇
* C++GUI Qt4编程--布兰切特
* Qt5.9 C++开发指南--王维波
* [【qt官网】](https://www.qt.io/cn/)
* [【pyqt官网】](https://www.riverbankcomputing.com/)
* [【pyqt入门教程】](https://blog.csdn.net/m0_57021623/article/details/123459038)
* [【界面切换参考自】](https://blog.csdn.net/weixin_43734095/article/details/106783108)
* [【背景图片设置参考自】](https://blog.csdn.net/qq_38161040/article/details/88363916)
* [【样式表参考自】](https://blog.csdn.net/zhouyingge1104/article/details/95377946)
* [【保存图片参考自】](https://blog.csdn.net/m0_47682721/article/details/123928585)
* [【进度条对话框参考自】](https://blog.csdn.net/yurensan/article/details/121025642)
* [【打开文件夹并读取文件列表参考自】](https://blog.csdn.net/weixin_45875105/article/details/113185870)
* [【多窗口数据传递参考自】](https://blog.csdn.net/jdl1206/article/details/121619463)
* [【pyinstaller打包和spec配置参考自】](https://blog.csdn.net/qq_38856833/article/details/115287480)
