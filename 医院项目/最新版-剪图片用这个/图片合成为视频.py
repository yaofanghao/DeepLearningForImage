import os
import cv2

if __name__ == '__main__':
    path = 'img_out/'  # 原图片的路径
    img_type = '.jpg'  # 原图片的格式
    video_name = 'kongbao.avi' # 保存视频的名称
    fps = 28.92 # 视频每秒帧数
    size = (544, 960)  # 需要转为视频的图片的尺寸，图片的尺寸多大，也可以使用cv2.resize()进行修改

    filelist = os.listdir(path)

    video = cv2.VideoWriter(video_name,
                            cv2.VideoWriter_fourcc(*'XVID'),
                            fps, size)

    #按顺序读取图片
    filelist.sort(key=lambda x: int(x.split('.')[0]))
    for item in filelist:
        if item.endswith(img_type):
            # 找到路径中所有后缀名为.jpg的文件，可以更换为.png或其它
            item = path + item
            img = cv2.imread(item)
            video.write(img)

    video.release()
    cv2.destroyAllWindows()