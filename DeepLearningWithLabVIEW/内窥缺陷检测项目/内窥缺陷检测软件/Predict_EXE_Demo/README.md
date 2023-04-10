# 源码 predict_for_exe.py
## 更新时间 2023.4.7 
* @yaofanghao
* 大致实现逻辑为： 
  * 1 逐帧分解视频到img文件夹中
  * 2 对img文件夹图片逐帧进行模型预测，只保存有预测结果的图片到img_out文件夹中 
  * 3 预测结果同时导出至txt或其他形式的文本
* 提高要求：
  * 1 优化程序结构，提升程序运行速度
  * 2 输出结果保存的地方值得考虑一下做改进
  * 3 输出结果的地方要和数据库相结合，labview后续可以调用数据库

# exe制作的简要说明
* 在要制作exe的文件夹下cmd，输入 
  * pyinstaller -F -i ./fac.ico tree.py
  * pyinstaller -F -c main.py 
    * -i./xxx.ico  是设置图标，选填
    * -F 打包为一个exe （-D不打包为一个exe，不推荐）
    * -c 带控制台，一般用于查找错误 （-w 不带控制台）
  * 示例：
    * pyinstaller -F -c predict_for_exe.py

* 生成结果： 
  * build文件夹
  * dist文件夹
  * 程序同名的spec文件
  * 保留dis中的.exe和需要运行的其他文件（如训练参数h5）即可，可转移到其他计算机运行