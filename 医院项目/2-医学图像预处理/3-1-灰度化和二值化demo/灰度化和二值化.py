import cv2
import os

base_dir = "./jpg"
out_gray_dir = "./gray/"
output_dir = './erzhihua/'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(out_gray_dir):
    os.makedirs(out_gray_dir)
	
filelist = os.listdir(base_dir)
filelist.sort(key=lambda x: int(x.split('.')[0]))
i = 1

for i in range(0, len(filelist)):
    path = os.path.join(base_dir, filelist[i])
    # print(path)

    save_path1 = out_gray_dir + str(i+1) + 'gray.jpg'  #保存至另一文件夹
    save_path = output_dir + str(i+1) + 'erzhihua.jpg'  #保存至另一文件夹

    img0 = cv2.imread(path, cv2.IMREAD_COLOR)  # 读取格式为BGR
    img = cv2.cvtColor(img0, cv2.COLOR_BGR2RGB)  # 转换为RGB
    gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)  # 转换为灰度图
    ret, mask = cv2.threshold(gray, 230, 255, 0) #简单二值化

    cv2.imwrite(save_path1, gray)
    cv2.imwrite(save_path, mask)
    print( i+1 )
