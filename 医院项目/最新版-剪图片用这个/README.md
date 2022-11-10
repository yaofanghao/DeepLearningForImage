# **更新日期**

2022.9.2

-------------------------------

labelme版本 3.16.2

**版本不同可能报错**

//
# **文件夹内含：**
* before-其中有class_name.txt，需检查无误
* output
* jpg 人名 未剪
* jpg1 数字 未剪
* jpg2 数字 第一次剪完
* jpg3 数字 第二次剪完
* jpg4 人名 第二次剪完
* png人名 未剪
* png1 数字 未剪
* png2 数字 第一次剪完
* png3 数字 第二次剪完
* png4 人名 第二次剪完
* 其他要用到的py文件

# **操作步骤：**
注意路径不要有中文名，否则程序可能会报错。

1.检查 class_name.txt 确保无误

2.json_to_dataset.py ，如果报错可切换环境，可能是labelme或pyqt版本问题

2.get_jpg_and_png.py，如果报错可能是class_name.txt中写错

3.复制jpg到jpg1，png到png1

4.yinshe.py（存至jpg1）

5.把jpg1中的name.txt移出

6.yinshe.py（存至png1）

7.把png1中的name.txt移出

8.lastsuanfa2.py（存至jpg2），此时生成了text1.txt。

9.cutpng2.py

10.lastsuanfa5.py（存至jpg3），此时生成了text2.txt

11.cutpng5.py

# **以下步骤先不进行（改回人名的处理）**
12.复制jpg3到jpg4

13.复制png3到png4

14.change_name.py（存至jpg4），需检查name.txt为UTF-8编码格式，每行有三个空格

15.change_name.py（存至png4）

16.结束。如需重新进行新一轮处理，需先删除三个txt文件。
