## 一、安装pipenv

代码：pip install pipenv

通过pipenv库来进入虚拟python环境，并将所在环境配置进入path中（或者在下面命令中指定所在路径）

## 二、安装虚拟环境并运行

代码：

pipenv install

pipenv shell

在所需文件夹位置打开cmd，输入上面命令进行虚拟环境搭建运行

## 三、放入运行所需库

代码：

pip install XXX

根据需要安装运行库

## 四、安装打包库：pyinstaller和UPX*

代码：

pipenv install pyinstaller

upx为压缩文件，可以进一步减少exe大小，选装，下载后解压到一个路径中并记录（下假定为D:\upx)

地址：[https://github.com/upx/upx/releases/tag/v4.2.2](https://github.com/upx/upx/releases/tag/v4.2.2)

## 五、实现打包

代码：

pyinstaller --upx-dir [D:\upx](D:\upx) -Fw XX.py -i XX.ico --clean 

-F表示打包成一个文件 -i选择图标 --clean清除缓存 -w隐藏命令行

--upx是使用压缩打包，也可以精简为：

```Shell
pyinstaller -Fw XX.py --clean
```



