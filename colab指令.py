#笔记本设置-gpu

from google.colab import drive
drive.mount("/content/drive") #获取验证码，挂在google drive

import os
path="/content/drive/MyDrive/untitled"
os.chdir(path)
os.listdir(path) #进入文件所在目录

!python test.py #运行py文件 
