import os
import cv2

path = 'img_out/'  # 原图片的路径
filelist = os.listdir(path)

fps = 28.92 # 视频每秒帧数
size = (544, 960)  # 需要转为视频的图片的尺寸，图片的尺寸多大
# 可以使用cv2.resize()进行修改

# 视频的名称为VideoTest1，格式为.avi
video = cv2.VideoWriter("kongpao.avi",
                        cv2.VideoWriter_fourcc(*'XVID'),
                        fps, size)
# 视频保存在当前目录下

#按顺序读取图片，这样保证是1,2,3...而不是1,10,11...
filelist.sort(key=lambda x: int(x.split('.')[0]))

for item in filelist:
    if item.endswith('.jpg'):
        # 找到路径中所有后缀名为.jpg的文件，可以更换为.png或其它
        item = path + item
        img = cv2.imread(item)
        video.write(img)

video.release()
cv2.destroyAllWindows()