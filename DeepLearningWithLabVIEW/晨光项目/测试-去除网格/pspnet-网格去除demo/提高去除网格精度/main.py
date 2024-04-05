# https://docs.opencv.org/4.x/d9/db0/tutorial_hough_lines.html

import sys
import math
import cv2 as cv
import numpy as np

def main(argv):
    default_file = 'test.jpg'
    predict_file = 'test1.jpg'
    src0 = cv.imread(default_file, cv.IMREAD_GRAYSCALE)
    src = np.copy(src0)
    mask = cv.imread(predict_file, cv.IMREAD_GRAYSCALE)
    mask_inv = cv.bitwise_not(mask)
    cv.imwrite("0-test1_inv.jpg", mask_inv)

    dst = cv.Canny(src0, 0, 150, None, 3)
    # cv.imshow("canny", dst)

    # Probabilistic Line Transform
    # 累计概率霍夫变换
    cdstP = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    # 用法：(image, rho, theta, threshold,
    #           lines=None, minLineLength=None, maxLineGap=None)
    linesP = cv.HoughLinesP(dst, 2, np.pi / 180, 150,
                            None, minLineLength=1, maxLineGap=1)

    # 画霍夫变换检测到的线（红色）
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            # (img, pt1, pt2, color, thickness=None, lineType=None, shift=None)
            cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 5, cv.LINE_AA)

    # # 阈值分割 mask
    # # 150以上的设为全黑
    # ret, mask = cv.threshold(src, 50, 255, 1) #简单二值化
    # cv.imwrite("1-mask.png",mask)

    # 对霍夫P变换检测到的线作为二次判断条件
    # print(cdstP[0,0,0])
    # print(cdstP.shape)
    # print(cdstP[1256,1257])
    # print(cdstP[1256,1257][2])
    for i in range(cdstP.shape[0]):
        for j in range(cdstP.shape[1]):

            # 对深度学习预测得到的图片中的白色部分排除为缺陷的可能，设置为白色
            # flag1 = (mask[i, j][0] == 255) & (mask[i, j][1] == 255) & (mask[i, j][2] == 255)
            flag1 = (mask[i, j] > 250)
            # 对霍夫P线检测中的红色部分排除为缺陷的可能，设置为白色
            flag2 = (cdstP[i, j][0] == 0) & (cdstP[i, j][1] == 0) & (cdstP[i, j][2] == 255)
            if flag1:
                src[i, j] = 255
            if flag2:
                src[i, j] = 255
            else:
                pass

    # Show results
    cv.namedWindow("Source", cv.WINDOW_NORMAL)
    cv.namedWindow("Predict result", cv.WINDOW_NORMAL)
    cv.namedWindow("Probabilistic Line Transform", cv.WINDOW_NORMAL)
    cv.namedWindow("Fianl result", cv.WINDOW_NORMAL)

    cv.imshow("Source", src0)
    cv.imshow("Predict result", mask)
    cv.imshow("Probabilistic Line Transform", cdstP)
    cv.imshow("Preprocess", src)

    mix = cv.add(src0, src)
    cv.namedWindow("Final-Result", cv.WINDOW_NORMAL)
    cv.imshow("Final-Result", mix)

    cv.imwrite("2-HoughLinesP.jpg", cdstP)
    cv.imwrite("3-preprocess.jpg", src)
    cv.imwrite("4-Final.jpg", mix)

    cv.waitKey()
    return 0

if __name__ == "__main__":
    main(sys.argv[1:])