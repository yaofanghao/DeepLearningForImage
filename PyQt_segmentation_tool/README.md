#### 语义分割训练前处理工具
详细说明在：[CSDN链接](https://blog.csdn.net/qq_39330520/article/details/108219002)
#### 运行
git clone或下载程序后，运行.exe文件可直接运行
或运行Segmentation_UI.py也可打开界面进行操作
#### 主要功能：
|  Num   |                         Title
|--------|------------------------------------------------------------
| FUNC1：| 视频素材转换成图像
| FUNC2：| 把标注后json文件和对应的jpg文件从混合的文件夹中提取出来
| FUNC3：| Json_to_Dataset功能.从Json文件获得标签文件
| FUNC4：| Get_JPG_PNG从上一步的Dataset文件中提取训练图像和训练标签
| FUNC5：| 从训练集中随机选取一定比例的图像和标签作为验证集图像和标签
| FUNC6：| 由模型输出标签和人工标签计算得到MIOU和MPA

#### BY LiangBo

#### FUNC1：视频素材转换成图像
* 用于将视频素材转换成单张图像素材，本程序默认转换为640*480大小的图像，若需其他尺寸需要在函数中修改

#### FUNC2：把标注后json文件和对应的jpg文件从混合的文件夹中提取出来.
* 当我们在用Labelme等标注素材图像时，往往将标注后的Json文件和这些素材放在同一个文件夹中.
  但又不需要对该文件夹中的每张图像都进行标注，因此在对Json和对应的Jpg文件进行Json_to_dataset之前需要
  将标注完成的Json文件及对应的Jpg文件提取出来单独存放，只就是FUN2的功能.
  
#### FUNC3：Json_to_Dataset功能
* 用于从标注完成的Json文件提取出来标签图像等信息存放到OUTPUT文件夹.

#### FUNC4：Get_JPG_PNG从上一步的Dataset文件中提取训练图像和训练标签
* 从Jpg文件夹和OUTPUT文件夹提取训练集的图像和标签文件分别存放到指定文件夹.

#### FUNC5：从训练集中随机选取一定比例的图像和标签作为验证集图像和标签
* 功能如标题所示.

#### FUNC6：由模型输出标签和人工标签计算得到MIOU和MPA
* 功能如标题所示.
  
![images](https://images.gitee.com/uploads/images/2020/0824/104232_a3ed91aa_5558625.png)
