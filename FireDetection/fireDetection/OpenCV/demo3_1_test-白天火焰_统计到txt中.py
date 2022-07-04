import cv2
import numpy as np
import os

###############################################
# 0测试图片，1测试视频
mode = 1

img_path = "imgfire/7.jpg"
out_path = './result/day/'
if not os.path.exists(out_path):
    os.makedirs(out_path)

video_path = "day.mp4"
video_save_path = "day_out.mp4"
video_fps = 30

# 参数设置
hl=0 # hsv的上下限
hh=30
sl=100
sh=255
vl=200
vh=255
kernal_size=5 # 开运算核的尺寸
conturs_ratio = 0.0001 # 初步识别出轮廓占图片总面积的比例
round_low = 0.2 # 圆形度下限
cntlen_low = 200 #圆形度上限

###############################################

def hsv_to_mask(img, hl,hh,sl,sh,vl,vh):
    # 转换到hsv空间，设定阈值生成mask
    # 关于阈值上下限的选取，参考 getHSV.py 获得大致范围
    # 输入 图片，hsv的三对上下限值
    # 输出 mask 和 hsv图片
    blur = cv2.GaussianBlur(img, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    a = [hl, sl, vl]  # 设置 h s v 的阈值上下限
    b = [hh, sh, vh]
    a = np.array(a, dtype="uint8")
    b = np.array(b, dtype="uint8")
    mask = cv2.inRange(hsv, a, b)
    return mask, hsv

def imgopen(mask, kernal_size):
    # 对mask做开运算
    # 输入 mask 和 结构元素尺寸
    # 输出 开运算后的 mask
    kernal2 = np.ones((kernal_size, kernal_size), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernal2)
    return mask

###############################################

if __name__ == '__main__':
    if mode == 0:

        img = cv2.imread(img_path)
        cv2.imwrite(out_path + '1.jpg', img)

        # hsv 阈值处理
        mask, hsv = hsv_to_mask(img, hl,hh,sl,sh,vl,vh)
        cv2.imshow('after_hsv', mask)
        cv2.waitKey()
        cv2.imwrite(out_path+'2.jpg', mask)

        # 开运算
        mask = imgopen(mask, kernal_size)
        cv2.imshow("after_mask", mask)
        cv2.waitKey()
        cv2.imwrite(out_path + '3.jpg', mask)

        # 融合处理
        output = cv2.bitwise_and(img, hsv, mask=mask)
        cv2.imshow('bitwise', output)
        cv2.waitKey()
        cv2.imwrite(out_path+'4.jpg', output)

        # 画轮廓
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        draw_img = cv2.drawContours(img, contours, -1, (0,0,255),5)
        cv2.imshow("result", draw_img)
        cv2.waitKey()
        cv2.imwrite(out_path+'5.jpg', draw_img)

        # 轮廓面积 圆形度 长度 特征
        # 考虑多个轮廓的情况
        img_area = img.shape[0] * img.shape[1]
        contoursImg = []
        cntLen = []
        num = 0
        print("总面积：",img_area)
        for i in range(len(contours)):
            temp = np.zeros(img.shape, np.uint8)
            contoursImg.append(temp)
            cntLen.append(cv2.arcLength(contours[i],True)) # 统计各轮廓长度
            roundIndex = 4 * 3.1415926 * cv2.contourArea(contours[i]) / ( cntLen[i] ** 2 + 0.00001)  # 圆形度 防止ZeroDivisionError
            roundIndex = round(roundIndex,3)
            print("轮廓" + str(i) + "面积:", cv2.contourArea(contours[i]))
            print("轮廓" + str(i) + "的圆形度为：" + str(roundIndex))
            print("轮廓" + str(i) + "的长度为：" + str(cntLen[i]))

            if (cv2.contourArea(contours[i]) > conturs_ratio * img_area) \
                    & (roundIndex > round_low) \
                    & (cntLen[i] > cntlen_low):  # 设置第二轮筛选的范围

                x, y, w, h = cv2.boundingRect(contours[i])
                draw_contours = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 5) # 绘制轮廓的最小外接矩形

                cv2.putText(img,'Warning!',(x, y),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),5)

                print("轮廓" + str(i) + "可能为火焰")
                print("轮廓" + str(i) + "的面积为:", cv2.contourArea(contours[i]))
                print("轮廓" + str(i) + "的圆形度为：" + str(roundIndex))
                print("轮廓" + str(i) + "的长度为:", cntLen[i])
                print('-------------------')

                num += 1

            else:
                draw_contours = cv2.rectangle(img, (0, 0), (1, 1), 1)

        cv2.imshow('draw_contours', draw_contours)

        cv2.waitKey()
        cv2.imwrite(out_path+'6.jpg', draw_contours)

        print("可能为火焰的个数:"+str(num))
        cv2.waitKey()
        cv2.destroyAllWindows()

        # #  背景消除（fmask显示为空白，暂未解决问题）
        # fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
        #
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # gray_frame = cv2.GaussianBlur(gray, (5, 5), 5)
        #
        # fmask = fgbg.apply(gray_frame)
        # kernel = np.ones((20, 20), np.uint8)
        # fmask = cv2.medianBlur(fmask, 3)
        # fmask = cv2.dilate(fmask, kernel)
        #
        # cv2.namedWindow("fmask", 2)
        # cv2.imshow('fmask', fmask)
        # cv2.waitKey()
        # cv2.imwrite(out_path+'4-fmask.jpg', fmask)


        # ret, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
        #
        # height, width = binary.shape
        # npframe = np.array(img)
        # # nphsv = np.array(hsv)
        # npbinary = np.array(binary)
        #
        # # 降噪
        # dst = cv2.medianBlur(binary, 5)
        #
        # # 开运算
        # kernal2 = np.ones((5, 5), np.uint8)
        # opening = cv2.morphologyEx(dst, cv2.MORPH_OPEN, kernal2)
        #
        # binary_x = 0
        # while binary_x < height:
        #     binary_y = 0
        #     while binary_y < width:
        #         if (opening[binary_x, binary_y] == 255):
        #             p = npframe[(binary_x, binary_y)]
        #
        #             if p[2] >= p[1] >= p[0]:  # & p2[2] >= 5:
        #                     binary_y += 1
        #                     continue
        #             else:
        #                 opening[binary_x, binary_y] = 0
        #         binary_y += 1
        #     binary_x += 1
        #
        # contour_img, contours, hierarchy = cv2.findContours(fmask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # for cnt in contours:
        #     x, y, w, h = cv2.boundingRect(cnt)
        #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #     smoke=1
        #     print(smoke)
        #
        # contour_img, contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # for cnt in contours:
        #     x, y, w, h = cv2.boundingRect(cnt)
        #     cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #     color=1
        #     print(color)
        #
        #
        # image, contour, hierarchy = cv2.findContours(opening,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # if contour == []:
        #     print('No contour')
        # else:
        #     #    Display outlines in the video window
        #     cv2.drawContours(img, contour, -1, (0, 0, 255), 2)
        #     inten=1
        #     print(inten)
        #
        # if smoke==1 and color==1 and inten==1 :
        #     res=1
        #     print(res)

    if mode == 1:
        cap = cv2.VideoCapture(video_path)

        if video_save_path != "":
            fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
            size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            out = cv2.VideoWriter(video_save_path, fourcc, video_fps, size)

        while True:
            ret, img = cap.read()
            if img is None:
                print("视频读取完成")
                break
            if not ret:
                raise ValueError("未识别视频（摄像头）")

            # hsv 分割
            mask, hsv = hsv_to_mask(img, hl,hh,sl,sh,vl,vh)
            # 开运算
            mask = imgopen(mask, kernal_size)
            # 融合
            output = cv2.bitwise_and(img, hsv, mask=mask)

            # 画轮廓
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            draw_img = cv2.drawContours(img, contours, -1, (0, 0, 255), 5)

            # 轮廓面积
            # 考虑多个轮廓的情况
            img_area = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) * int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            contoursImg = []
            cntLen = []
            num = 0

            # 创建txt，火焰信息保存到txt中
            f = open(os.path.join(os.getcwd() + 'fire_report.txt'), 'a')

            for i in range(len(contours)):
                temp = np.zeros(img.shape, np.uint8)
                contoursImg.append(temp)
                cntLen.append(cv2.arcLength(contours[i], True))  # 统计各轮廓长度
                roundIndex = 4 * 3.1415926 * cv2.contourArea(contours[i]) / (cntLen[i] ** 2 + 0.00001) # 圆形度 防止ZeroDivisionError
                roundIndex = round(roundIndex, 3)
                if (cv2.contourArea(contours[i]) > conturs_ratio * img_area) \
                        & (roundIndex > round_low) \
                        & (cntLen[i] > cntlen_low):  # 设置第二轮筛选的范围

                    x, y, w, h = cv2.boundingRect(contours[i])
                    draw_contours = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 5)

                    cv2.putText(img, 'Warning!', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)

                    print("轮廓" + str(i) + "可能为火焰")
                    print("轮廓" + str(i) + "的面积为:", cv2.contourArea(contours[i]))
                    print("轮廓" + str(i) + "的圆形度为：" + str(roundIndex))
                    print("轮廓" + str(i) + "的长度为:", cntLen[i])
                    print('-------------------')

                    f.write(str(cv2.contourArea(contours[i]))+"\t"+\
                                str(roundIndex)+"\t"+\
                                str(cntLen[i])+"\t")
                    f.write("\r")

                    num += 1

                else:
                    draw_contours = cv2.rectangle(img, (0,0), (1,1), 1)

            cv2.imshow('draw_contours', draw_contours)
            c= cv2.waitKey(1) & 0xff
            print("可能为火焰的个数:" + str(num))

            if video_save_path != "":
                out.write(draw_contours)

            if c==27:
                cap.release()
                break

        print("视频处理完成")
        cap.release()

        if video_save_path!="":
            print("Save processed video to the path :" + video_save_path)
            out.release()
        cv2.destroyAllWindows()