import cv2
import os

video_name = '2'

output_dir = 'img/'

vc = cv2.VideoCapture(video_name + '.mp4')  # 读入视频文件

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

if vc.isOpened():  # 判断是否正常打开
    rval , frame = vc.read()
else:
    rval = False
    print('Video do not exist.')

timeF = 1  # 视频帧计数间隔频率
c = 1  # 统计帧数
while rval:   # 循环读取视频帧
    rval, frame = vc.read()
    print(rval, frame)
    if c % timeF == 0:  # 每隔timeF帧进行存储操作
        cv2.imwrite(output_dir + str(c) + '.jpg', frame)  # 存储为图像
    c = c + 1
    cv2.waitKey(1)
    print('success:' + str(c))
vc.release()
