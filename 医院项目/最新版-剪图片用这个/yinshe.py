#批量修改文件名
#批量修改图片文件名
import os
import re
import sys
def renameall():
	fileList = os.listdir(r"E:\MyGithub\DeepLearningForImage\医院项目\2-医学图像预处理\4-边缘检测对比\img1")		#待修改文件夹
	saveBasePath = r"E:\MyGithub\DeepLearningForImage\医院项目\2-医学图像预处理\4-边缘检测对比\img1"
	print("修改前："+str(fileList))		#输出文件夹中包含的文件
	print("---------------------------------------------------")
	T = str(fileList)
	print(T)
	currentpath = os.getcwd()		#得到进程当前工作目录
	os.chdir(r"E:\MyGithub\DeepLearningForImage\医院项目\2-医学图像预处理\4-边缘检测对比\img1")		#将当前工作目录修改为待修改文件夹的位置
	num=1
	#名称变量
	##顺序
	filelist = os.listdir(saveBasePath)
	# filelist.sort(key=lambda x: int(x[:-4]))
	for fileName in fileList:		#遍历文件夹中所有文件
		print(fileName)
		pat=".+\.(jpg|png|gif|json|JPG|xml)"		#匹配文件名正则表达式
		pattern = re.findall(pat,fileName)		#进行匹配
		os.rename(fileName,(str(num)+'.'+pattern[0]))		#文件重新命名

		ftrainval=open(os.path.join(saveBasePath, 'name.txt'), 'a')
		ftrainval.write(str(num))
		ftrainval.write(' ')
		ftrainval.write(fileName)
		ftrainval.write("\r")

		print(num)
		num = num+1		#改变编号，继续下一项

renameall()