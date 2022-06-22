#批量修改文件名
#批量修改图片文件名
import os
import re
import sys
def renameall():
	saveBasePath = r"C:\Users\姚方浩\Desktop\重命名\jpgcmm"
	fileList = os.listdir(saveBasePath)		#待修改文件夹

	fileList.sort(key=lambda x: int(x.split('.')[0]))

	print("修改前："+str(fileList))		#输出文件夹中包含的文件
	print("---------------------------------------------------")
	T = str(fileList)
	print(T)
	currentpath = os.getcwd()		#得到进程当前工作目录
	os.chdir(saveBasePath)		#将当前工作目录修改为待修改文件夹的位置
	num=1		#名称变量
	for fileName in fileList:		#遍历文件夹中所有文件

		pat=".+\.(jpg|png|gif|json|JPG)"		#匹配文件名正则表达式
		pattern = re.findall(pat,fileName)		#进行匹配
		os.rename(fileName,(str(num)+'.'+pattern[0]))		#文件重新命名

		ftrainval=open(os.path.join('name.txt'), 'a')
		ftrainval.write(str(num))
		ftrainval.write(' ')
		ftrainval.write(fileName)
		ftrainval.write("\r")


		#print("---------------------------------------------------")
		#print(fileName)

		print(num)
		num = num+1		#改变编号，继续下一项

	#print("---------------------------------------------------")
	#os.chdir(currentpath)		#改回程序运行前的工作目录
	#sys.stdin.flush()		#刷新
	#print("修改后："+str(os.listdir(r"C:\Users\Lenovo\Desktop\1月2号\测试映射\图片测试\图\修改后jpg")))		#输出修改后文件夹中包含的文件
renameall()