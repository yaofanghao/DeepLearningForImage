#批量修改文件名
#批量修改图片文件名
import os
import re
import sys

if __name__ == '__main__':
	saveBasePath = r"C:\Users\姚方浩\Desktop\重命名\jpgcmm" # 待重命名成数字的文件夹
	fileList = os.listdir(saveBasePath)		

	fileList.sort(key=lambda x: int(x.split('.')[0]))

	# print("修改前："+str(fileList))		
	T = str(fileList)
	# print(T)
	currentpath = os.getcwd()		#得到进程当前工作目录
	os.chdir(saveBasePath)		#将当前工作目录修改为待修改文件夹的位置
	num=1		#名称变量
	for fileName in fileList:		#遍历文件夹中所有文件
		pat=".+\.(jpg|png|gif|json|JPG)"		#匹配文件名正则表达式
		pattern = re.findall(pat,fileName)		#进行匹配
		os.rename(fileName,(str(num)+'.'+pattern[0]))		#文件重命名
		ftrainval=open(os.path.join('name.txt'), 'a')
		ftrainval.write(str(num))
		ftrainval.write(' ')
		ftrainval.write(fileName)
		ftrainval.write("\r")
		#print(fileName)
		print(num)
		num = num+1		#改变编号，继续下一项