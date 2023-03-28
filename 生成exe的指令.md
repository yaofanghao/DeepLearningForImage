## 在要制作exe的文件夹下cmd，输入

* **pyinstaller -F -i ./fac.ico tree.py**
  或
* **pyinstaller -F -c main.py**
  * -i./xxx.ico  是设置图标，选填
  * -F 打包为一个exe （-D不打包为一个exe，不推荐）
  * -c 带控制台，一般用于查找错误 （-w 不带控制台）
  
* 生成结果：
  * build文件夹
  * dist文件夹程序
  * 同名的spec文件
  
* 保留dis中的.exe和需要运行的其他文件（如训练参数h5）即可，可以转移到其他计算机运行。
* **在同一目录下放入upx.exe可以减少一些生成exe的大小**

* 如果提示 A RecursionError (maximum recursion depth exceeded) occurred.For working around please follow these instructions ，在spec文件中开头加入以下两行：
import sys
sys.setrecursionlimit(2000)
* 然后cmd下输入
pyinstaller xxx.spec