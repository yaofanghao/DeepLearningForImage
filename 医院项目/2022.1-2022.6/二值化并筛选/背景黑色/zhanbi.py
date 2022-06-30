import cv2
import numpy as np

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
    cv2.putText(dst, "area/sum:" + str(area / image.size)*100, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, .7, (255, 0, 0), 2)  # 显示
    print((area / image.size)*100)
    cv2.imshow("t3", dst)
    cv2.waitKey(0)

src = cv2.imread("8.jpg")
edge_output = edge_demo(src)
edge_area(edge_output)
