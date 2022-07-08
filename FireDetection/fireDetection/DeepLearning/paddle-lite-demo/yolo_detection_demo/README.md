## 针对火焰检测修改的代码

更新时间 2022.7.8
参考资料：
* https://paddle-lite.readthedocs.io/zh/develop/user_guides/cpp_demo.html
* https://github.com/PaddlePaddle/Paddle-Lite-Demo/tree/master/PaddleLite-armlinux-demo

## run.sh
* 
* ./yolo_detection_demo ../models/yolov3_darknet53_opt.nb ../labels/fire_label.txt ../images/1.jpg ./result.jpg
* 格式
  * ./yolov3_detection_demo model_dir label_path [input_image_path] [output_image_path]
  * use images from camera if input_image_path and output_image_path are not provided.

## yolo_detection_demo.cc
* 进入main函数，输入参数必须为 3个 或 5个
* log、paddle初始化
* 读取 图片 或 摄像头 
  * --> process函数 
    * 设置输入数据，调用 preprocess，将图片格式转换 BGR2RGB NHWC2NCHW
  * 预测
  * 获取输出数据
  * 后处理，调用 postprocess 获得框的坐标位置、类别、置信度等

## 后续工作
* 增加串口通信serial模块