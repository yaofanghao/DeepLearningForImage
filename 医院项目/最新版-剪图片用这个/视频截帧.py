import cv2
import os

if __name__ == '__main__':
    video_name = 'video3.mp4' # 原视频名称
    output_dir = 'img/' # 保存图片路径
    output_img_type = '.jpg' # 保存图片的格式

    vc = cv2.VideoCapture(video_name)  
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if vc.isOpened():  
        rval , frame = vc.read()
    else:
        rval = False
        print('Video do not exist.')

    timeF = 1  # 视频帧计数间隔频率
    c = 1  # 统计帧数
    while rval:   # 循环读取视频帧
        rval, frame = vc.read()
        print(rval, frame)
        if c % timeF == 0:  # 每隔timeF帧进行存储
            cv2.imwrite(output_dir + str(c) + output_img_type, frame)  
        c = c + 1
        cv2.waitKey(1)
        print('success:' + str(c))
    vc.release()
