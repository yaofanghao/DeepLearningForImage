# 读取图片，读取xml文件
# 解析xml文件获取图片的大小，xml中的多组坐标
# 翻转图片，根据图片翻转的角度，获取新的图片大小和坐标点
# 将坐标信息和图片大小在原有的xml中修改参数保存到新的xml文件中
# 创建新的文件夹，将图片和xml文件放在同一文件夹中（一组图片和xml文件命名相同）
 
import os
import numpy as np
import cv2
import math
import xml.etree.ElementTree as ET
 
#按角度翻转图片
def rotate_img(src, angle, scale = 1):
	width = src.shape[1]
	height = src.shape[0]
	# 角度变弧度
	re_angle = np.deg2rad(angle)
	# 计算新图片的高度和宽度
	new_width = (abs(np.sin(re_angle) * height) + abs(np.cos(re_angle) * width)) * scale
	new_height = (abs(np.cos(re_angle) * height) + abs(np.sin(re_angle) * width)) * scale
 
	rotate_matrix = cv2.getRotationMatrix2D((new_width * 0.5, new_height * 0.5), angle, scale)
	rotate_move = np.dot(rotate_matrix, np.array([(new_width - width) * 0.5, (new_height - height) * 0.5, 0]))
 
	# update translation
	rotate_matrix[0, 2] += rotate_move[0]
	rotate_matrix[1, 2] += rotate_move[1]
 
	dst = cv2.warpAffine(img, rotate_matrix, (int(math.ceil(new_width)), int(math.ceil(new_height))), flags=cv2.INTER_LANCZOS4)
	return dst
 
# 翻转后的xml文件信息
def rotate_xml(src, xmin, ymin, xmax, ymax, angle, scale = 1):
	width = src.shape[1]
	height = src.shape[0]
	re_angle = np.deg2rad(angle)
	new_width = (abs(np.sin(re_angle) * height) + abs(np.cos(re_angle) * width)) * scale
	new_height = (abs(np.cos(re_angle) * height) + abs(np.sin(re_angle) * width)) * scale
	rotate_matrix = cv2.getRotationMatrix2D((new_width * 0.5, new_height * 0.5), angle, scale)
	rotate_move = np.dot(rotate_matrix, np.array([(new_width - width) * 0.5, (new_height - height) * 0.5, 0]))
	rotate_matrix[0, 2] += rotate_move[0]
	rotate_matrix[1, 2] += rotate_move[1]
	# 获取原始矩形的四个中点，然后将这四个点转换到旋转后的坐标系下
	point1 = np.dot(rotate_matrix, np.array([(xmin + xmax) / 2, ymin, 1]))
	point2 = np.dot(rotate_matrix, np.array([xmax, (ymin + ymax) / 2, 1]))
	point3 = np.dot(rotate_matrix, np.array([(xmin + xmax) / 2, ymax, 1]))
	point4 = np.dot(rotate_matrix, np.array([xmin, (ymin + ymax) / 2, 1]))
	concat = np.vstack((point1, point2, point3, point4))  # 合并np.array
	# 改变array类型
	concat = concat.astype(np.int32)
	rx, ry, rw, rh = cv2.boundingRect(concat)		#rx,ry,为新的外接框左上角坐标，rw为框宽度，rh为高度
	new_xmin = rx
	new_ymin = ry
	new_xmax = rx + rw
	new_ymax = ry + rh
 
	return new_xmin, new_ymin, new_xmax, new_ymax
 
if __name__ == '__main__':
 
	file_path = 'E:\\MyGithub\\xmltest\\test\\' #输入路径，同时有jpg和xml文件
	rotated_img_path = 'E:\\MyGithub\\xmltest\\jpg2\\'	 #翻转后的图片路径
	rotated_xml_path = 'E:\\MyGithub\\xmltest\\xml2\\'  #翻转后的xml路径
	if not os.path.exists(rotated_img_path):
		os.makedirs(rotated_img_path)
	if not os.path.exists(rotated_xml_path):
		os.makedirs(rotated_xml_path)
 
	# 自定义翻转角度
	for angle in (90,180,270):
		for file in os.listdir(file_path):
			if file.endswith('.jpg'):
				a,b = os.path.splitext(file)
				img = cv2.imread(file_path + a + '.jpg')
				rotated_img = rotate_img(img, angle)
				cv2.imwrite(rotated_img_path + a + '_' + str(angle) + 'd.jpg', rotated_img)
				print(str(file) + ' ' + 'has been rotated for' + str(angle) + '°')
			if file.endswith('.xml'):
				src = cv2.imread(file_path + a + '.jpg')
				tree = ET.parse(file_path + a + '.xml')
				root = tree.getroot()
				# 修改xml中的标签坐标信息
				for box in root.iter('bndbox'):
					xmin = float(box.find('xmin').text)
					ymin = float(box.find('ymin').text)
					xmax = float(box.find('xmax').text)
					ymax = float(box.find('ymax').text)
					new_xmin, new_ymin, new_xmax, new_ymax = rotate_xml(src, xmin, ymin, xmax, ymax, angle)
					box.find('xmin').text = str(new_xmin)
					box.find('ymin').text = str(new_ymin)
					box.find('xmax').text = str(new_xmax)
					box.find('ymax').text = str(new_ymax)
				tree.write(rotated_xml_path + a + '_' + str(angle) + 'd.xml')
				print(str(file) + ' ' + 'has been rotated for ' + str(angle) + '°')
 
	print("-----------------------------------")
	print("Successful!")