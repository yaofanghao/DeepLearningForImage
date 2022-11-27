## 2022.9.22-
## 更新时间 2022.11.24

* 实现了将肠化亚型预测结果自动按照最大分数归类至三种文件夹：
	- CIM
	- IIM
	- fail
* 打印预测结果和准确率
* 目前适用于： YOLOv3、 Faster-RCNN、 SSD
* 未测试：mobilenet-yolov4、centernet、DETR等

* 查找Faster-RCNN改进方法，用于大论文
	* 改进backbone，如resnet101，mobilenet等
	* 改进分类回归层，包括通过多层来提取特征和判别
	
## 参考资料
* https://paperswithcode.com/task/medical-image-classification
