import cv2
import os

output_dir = './erzhihua/'  # 二值化处理后存放的文件夹位置

def edge_demo(image):
    blurred = cv2.GaussianBlur(image, (3, 3), 0)  # 高斯模糊降噪
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)  # 灰度图
    edge_output = cv2.Canny(gray, 50, 150)  # 不求梯度也可以
    return edge_output

def edge_area(image):
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 轮廓发现
    dst = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(dst, contours, -1, (0, 0, 255), 3)  # 画出轮廓
    area = 0
    for c in range(len(contours)):
        area += cv2.contourArea(contours[c])  # 面积
    # cv2.putText(dst, "area/sum:" + str(area / image.size)*100, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, .7, (255, 0, 0), 2)  # 显示
    # cv2.imshow("t3", dst)
    # cv2.waitKey(0)
    zhanbi = (area / image.size)*100


    ######################
    # x, y = image.shape
    # # print(image.shape)
    # for i in range(x):
    #     for j in range(y):
    #         if image[i, j] > 0:
    #             image[i, j] = 255
    #         else:
    #             image[i, j] = 0
    # black = 0
    # white = 0
    # # 遍历二值图，为0则black+1，否则white+1
    # for i in range(x):
    #     for j in range(y):
    #         if image[i, j] == 0:
    #             black += 1
    #         else:
    #             white += 1
    # print("白色个数:", white)
    # print("黑色个数:", black)
    # rate1 = white / (x * y)
    # rate2 = black / (x * y)
    # print(white + black)
    #
    # rate1 = white / (white + black)
    # rate2 = black / (white + black)
    #
    # print("白色占比:", round(rate1 * 100, 2), '%')
    # print("黑色占比:", round(rate2 * 100, 2), '%')
    # return rate1
    return zhanbi


filelist2 = os.listdir(output_dir)
filelist2.sort(key=lambda x: int(x.split('.')[0]))
i = 1
for i in range(0, len(filelist2)):
    path2 = os.path.join(output_dir, filelist2[i])
    src = cv2.imread(path2)
    edge_output = edge_demo(src)
    zhanbi = edge_area(edge_output)

    file = open(r'zhanbi.txt', mode='a')  # 将空格写入txt文件中
    file.write(filelist2[i])
    file.write(' ')
    file.write(str(zhanbi))
    file.write(' ')
    file.write('\n')  # 将回车写入txt文件中
    file.close()

    print('统计占比中：' + str(i+1))
