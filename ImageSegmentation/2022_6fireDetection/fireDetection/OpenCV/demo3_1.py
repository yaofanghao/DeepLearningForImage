import cv2
import numpy as np
import os

###############################################
# 0测试图片，1测试视频
mode = 0

img_path = "img/1.jpg"
out_path = './demo3_1_result/'
if not os.path.exists(out_path):
    os.makedirs(out_path)

video_path = "video3.mp4"
video_save_path = "video3out.mp4"
video_fps = 30

###############################################

if mode == 0:
    ############# 第一步 #################
    # 转换到hsv空间，设定阈值生成mask
    # 关于阈值上下限的选取，参考 getHSV.py 获得大致范围
    img = cv2.imread(img_path)
    cv2.imwrite(out_path + '1-origin.jpg', img)
    img_area = img.shape[0] * img.shape[1]
    # print(img_area)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    blur = cv2.GaussianBlur(img, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    a = [0, 80, 200]  # 设置 h s v 的阈值上下限
    b = [20, 255, 230]
    a = np.array(a, dtype="uint8")
    b = np.array(b, dtype="uint8")
    mask = cv2.inRange(hsv, a, b)

    # 显示hsv阈值处理后结果
    cv2.imshow('after_hsv', mask)
    cv2.waitKey()
    cv2.imwrite(out_path+'2-after_hsv.jpg', mask)

    output = cv2.bitwise_and(img, hsv, mask=mask)

    cv2.imshow('bitwise', output)
    cv2.waitKey()
    cv2.imwrite(out_path+'3-bitwise.jpg', output)

    ############# 第二步 #################
    # 开运算



    # 画轮廓
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    draw_img = cv2.drawContours(img, contours, -1, (0,0,255),5)
    cv2.imshow("result", draw_img)
    cv2.waitKey()
    cv2.imwrite(out_path+'4-output.jpg', draw_img)

    # 轮廓面积和圆形度特征
    # 考虑多个轮廓的情况
    contoursImg = []
    cntLen = []
    num = 0
    for i in range(len(contours)):

        temp = np.zeros(img.shape, np.uint8)
        contoursImg.append(temp)
        cntLen.append(cv2.arcLength(contours[i],True)) # 统计各轮廓长度
        print("轮廓" + str(i) + "面积:", cv2.contourArea(contours[i]))
        roundIndex = 4 * 3.1415926 * cv2.contourArea(contours[i]) / ( cntLen[i] ** 2 + 0.00001)  # 圆形度 防止ZeroDivisionError
        print("轮廓" + str(i) + "的圆形度为：" + str(roundIndex))

        if (cv2.contourArea(contours[i]) > 0.002 * img_area) \
                & (roundIndex > 0.2) \
                & (cntLen[i] > 500):  # 只有轮廓大于某一面积，圆形度小于某一值 才会识别出来

            x, y, w, h = cv2.boundingRect(contours[i])
            draw_contours = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 5) # 绘制轮廓的最小外接矩形

            roundIndex = 4*3.1415926* cv2.contourArea(contours[i]) / (cntLen[i]**2)
            print("轮廓" + str(i) + "可能为火焰")
            print("轮廓" + str(i) + "的面积为:", cv2.contourArea(contours[i]))
            print("轮廓" + str(i) + "的圆形度为：" + str(roundIndex))
            print("轮廓" + str(i) + "的长度为:", cntLen[i])
            print('-------------------')

            num += 1

        else:
            draw_contours = cv2.rectangle(img, (0, 0), (1, 1), 1)

        print("可能为火焰的目标数:" + str(num))
        cv2.imshow('draw_contours', draw_contours)

    cv2.waitKey()
    cv2.imwrite(out_path+'5-draw_contours.jpg', draw_contours)

    # for cnt in contours:
    #     x, y, w, h = cv2.boundingRect(cnt)
    #     cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    #     color=1
    #     print(color)
    print("可能为火焰的目标数:"+str(num))
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

        # 转换到hsv空间，设定阈值生成mask
        # 关于阈值上下限的选取，参考 getHSV.py 获得大致范围
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        blur = cv2.GaussianBlur(img, (21, 21), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        a = [0, 80, 200]  # 设置 h s v 的阈值上下限
        b = [30, 255, 230]
        a = np.array(a, dtype="uint8")
        b = np.array(b, dtype="uint8")
        mask = cv2.inRange(hsv, a, b)

        output = cv2.bitwise_and(img, hsv, mask=mask)

        # 开运算

        # 画轮廓
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        draw_img = cv2.drawContours(img, contours, -1, (0, 0, 255), 5)

        # 轮廓面积
        # 考虑多个轮廓的情况
        contoursImg = []
        cntLen = []
        num = 0
        for i in range(len(contours)):

            temp = np.zeros(img.shape, np.uint8)
            contoursImg.append(temp)
            img_area = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) * int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cntLen.append(cv2.arcLength(contours[i], True))  # 统计各轮廓长度
            roundIndex = 4 * 3.1415926 * cv2.contourArea(contours[i]) / (cntLen[i] ** 2 + 0.00001) # 圆形度 防止ZeroDivisionError

            if (cv2.contourArea(contours[i]) > 0.002 * img_area)\
                    & (roundIndex > 0.2) \
                    & (cntLen[i] > 500):  # 只有轮廓大于某一面积，圆形度小于某一值 才会识别出来

                x, y, w, h = cv2.boundingRect(contours[i])
                draw_contours = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 5)

                print("轮廓" + str(i) + "可能为火焰")
                print("轮廓" + str(i) + "的面积为:", cv2.contourArea(contours[i]))
                print("轮廓" + str(i) + "的圆形度为：" + str(roundIndex))
                print("轮廓" + str(i) + "的长度为:", cntLen[i])
                print('-------------------')

                num += 1

            else:
                draw_contours = cv2.rectangle(img, (0,0), (1,1), 1)

        print("可能为火焰的目标数:" + str(num))

        cv2.imshow('draw_contours', draw_contours)
        c= cv2.waitKey(1) & 0xff
        if video_save_path != "":
            out.write(draw_contours)

        if c==27:
            cap.release()
            break

    print("Video Detection Done!")
    cap.release()

    if video_save_path!="":
        print("Save processed video to the path :" + video_save_path)
        out.release()
    cv2.destroyAllWindows()