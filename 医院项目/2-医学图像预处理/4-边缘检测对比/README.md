# 操作流程
* 2022.11.2 


**路径中不能有中文名，否则会出现难以解决的报错!!!**

# 进度
* 我们的方法：运行lastsuanfa2.py 已完成
* 对比代码，用以下四种替换lastsuanfa2.py：/ 已完成
  * sobel：运行lastsuanfa2-sobel.py / 已完成
  * canny：运行lastsuanfa2-canny.py / 已完成
  * roberts：运行lastsuanfa2-roberts.py / 已完成
  * prewitt：运行lastsuanfa2-prewitt.py / 已完成

# 使用流程
* 1、需要预先准备
    img1文件夹 重命名为数字的原图

* 2、粗剪，运行lastsuanfa2.py，得到：
    * 2-sobel_horizontal文件夹 存放sobel_horizontal图
    * 3-suanfa2文件夹 存放lastsuanfa2剪完的图
    
* 3、精剪，运行lastsuanfa5.py，得到：
    * 4-canny文件夹 存放canny图
    * 5-juxing文件夹 存放juxing图
    * 6-suanfa5文件夹 存放lastsuanfa5剪完的图
  
