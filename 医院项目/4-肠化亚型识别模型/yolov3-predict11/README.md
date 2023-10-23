### 更新时间 2022.6.29

### predict11.py代码说明
**该版本实现了统计分类结果、线性变换修改生成的置信度、自动标注等功能**

**代码需要调用** 
* **gen_xml.py** 
* **yolo_predict3.py**

**!!运行前检查!!**
* gen_xml.py 和 yolo_predict3.py 是否存在
* logs中权重是否选取正确
* model_data 中 voc_classes.txt 是否正确
	
**运行完生成内容**
* 文件夹：

        img_out_all_NEO 
            ————识别为癌症的图片
        img_out_all_NONNEO  
            ————识别为非癌症的图片
        img_out_fail 
            ————未识别出框的图片
        Annotations 
            ————上述三个文件夹所有图片预测结果的xml标签文件 
* txt文档：
  
        0.05_predict_report.txt
            ————包含未识别率、灵敏度、特异度等信息
        0.05_predict_report2.txt
            ————如果预测结果有癌症，打印这些图片癌症的框的最大分数
        0.05_predict_report3.txt
            ————如果预测结果混合，打印这些图片癌症框和非癌症框的最大分数
        result.txt 
            ————打印所有图片预测的类别、框的四个坐标点信息
        fail.txt
            ————打印没有预测结果的图片名称
        new_scores.txt
            ————打印所有图片预测分数进行线性变换后的结果