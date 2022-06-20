import cv2
import numpy as np
import os

img_path = "img/1.jpg"
out_path = './demo3_1_result/'
if not os.path.exists(out_path):
    os.makedirs(out_path)

img = cv2.imread(img_path)
cv2.imwrite(out_path+'1-origin.jpg', img)
img_area = img.shape[0]*img.shape[1]
# print(img_area)

############# 第一步 #################
# 转换到hsv空间，设定阈值生成mask
# 关于阈值上下限的选取，参考 getHSV.py 获得大致范围
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
blur = cv2.GaussianBlur(img, (21, 21), 0)
hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
a = [0, 80, 200]  # 设置 h s v 的阈值上下限
b = [20, 255, 230]
a = np.array(a, dtype="uint8")
b = np.array(b, dtype="uint8")
mask = cv2.inRange(hsv, a, b)

# 显示hsv阈值处理后结果
cv2.namedWindow("before_hsv", 0)
cv2.imshow('before_hsv', mask)
cv2.waitKey()
cv2.imwrite(out_path+'2-before_hsv.jpg', mask)

output = cv2.bitwise_and(img, hsv, mask=mask)

cv2.namedWindow("before_hsv_bitwise", 1)
cv2.imshow('before_hsv_bitwise', output)
cv2.waitKey()
cv2.imwrite(out_path+'3-before_hsv_bitwise.jpg', output)

############# 第二步 #################
# 开运算






# 画轮廓
contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
draw_img = cv2.drawContours(img, contours, -1, (0,0,255),5)
cv2.imshow("result", draw_img)
cv2.waitKey()
cv2.imwrite(out_path+'output.jpg', draw_img)

# 轮廓面积
# 考虑多个轮廓的情况
contoursImg = []
num = 0
for i in range(len(contours)):
    print("轮廓" + str(i) + "面积:", cv2.contourArea(contours[i]))
    temp = np.zeros(img.shape, np.uint8)
    contoursImg.append(temp)
    if cv2.contourArea(contours[i]) > 0.001*img_area:  # 只有轮廓大于某一面积才会识别出来
        print("轮廓" + str(i) + "可能为火焰")
        contoursImg[i] = cv2.drawContours(contoursImg[i], contours, i, (0, 0, 255), 5)
        x, y, w, h = cv2.boundingRect(contours[i])
        contoursImg[i] = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)
        cv2.imshow(str(i), contoursImg[i])
        num += 1

# for cnt in contours:
#     x, y, w, h = cv2.boundingRect(cnt)
#     cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
#     color=1
#     print(color)
print("可能为火焰的目标数:"+str(num))
cv2.waitKey()
cv2.destroyAllWindows()

# 轮廓的圆形度





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




# 视频处理
# while True:
#     (grabbed, frame) = video.read()
#     if not grabbed:
#         break

#     blur = cv2.GaussianBlur(frame, (21, 21), 0)
#     hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
#     # h, s, i, hsi = rgb2hsi(frame)

#     # 根据情况需要调整阈值上下限
#     lower = [0, 20, 100]
#     upper = [20, 100, 255]

#     lower = np.array(lower, dtype="uint8")
#     upper = np.array(upper, dtype="uint8")
#     mask = cv2.inRange(hsv, lower, upper)
#     # mask = cv2.inRange(hsi, lower, upper)

#     output = cv2.bitwise_and(frame, hsv, mask=mask)
#     no_red = cv2.countNonZero(mask)
#     # output = cv2.bitwise_and(frame, hsi, mask=mask)
#     # no_red = cv2.countNonZero(mask)

#     cv2.imshow("output", output)
#     print("output:", frame)
#     if int(no_red) > 20000:
#         print('Fire detected')
#     # print(int(no_red))
#     # print("output:".format(mask))
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cv2.destroyAllWindows()
# video.release()