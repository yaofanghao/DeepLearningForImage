# https://docs.opencv.org/4.x/d9/db0/tutorial_hough_lines.html

import sys
import math
import cv2 as cv
import numpy as np

def main(argv):
    default_file = 'test.bmp'
    filename = argv[0] if len(argv) > 0 else default_file

    src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_GRAYSCALE)

    if src is None:
        print ('Error opening image!')
        print ('Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
        return -1

    # Edge detection
    dst = cv.Canny(src, 0, 150, None, 3)
    cv.imshow("canny",dst)

    cdstP = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    # cdstP = np.copy(cdst)

    #  Standard Hough Line Transform
    # rho: 参数的分辨率r以像素为单位
    # 返回值lines为结构体数组，包含端点1、2, 角度, rho
    # lines = cv.HoughLines(dst, 10, np.pi / 180,
    #                       150, None, 0, 0)

    # # Draw the lines
    # if lines is not None:
    #     for i in range(0, len(lines)):
    #         rho = lines[i][0][0]
    #         theta = lines[i][0][1]
    #         a = math.cos(theta)
    #         b = math.sin(theta)
    #         x0 = a * rho
    #         y0 = b * rho
    #         pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
    #         pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
    #         cv.line(cdst, pt1, pt2, (0,0,255), 3, cv.LINE_AA)

    # Probabilistic Line Transform
    # 累计概率霍夫变换
    # 用法：(image, rho, theta, threshold,
    #           lines=None, minLineLength=None, maxLineGap=None)
    linesP = cv.HoughLinesP(dst, 2, np.pi / 180, 50,
                            None, 500, 10)

    # Draw the lines
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            # (img, pt1, pt2, color, thickness=None, lineType=None, shift=None)
            cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 5, cv.LINE_AA)

    # 阈值分割 mask
    # 150以上的设为全黑
    ret, mask = cv.threshold(src, 50, 255, 1) #简单二值化
    cv.imwrite("1-mask.png",mask)

    # 对霍夫P变换检测到的线作为二次判断条件
    # print(cdstP[0,0,0])
    # print(cdstP.shape)
    # print(cdstP[1256,1257])
    # print(cdstP[1256,1257][2])
    for i in range(cdstP.shape[0]):
        for j in range(cdstP.shape[1]):
            # 对于阈值分割结果mask：如果认为是网格，像素值设置为0（全黑）；否则不处理
            flag = (cdstP[i, j][0] == 0) & (cdstP[i, j][1] == 0) & (cdstP[i, j][2] == 255)
            if flag:
                mask[i, j] = 0
            else:
                pass

    # Show results
    cv.namedWindow("Source", cv.WINDOW_NORMAL)
    cv.namedWindow("Probabilistic Line Transform", cv.WINDOW_NORMAL)
    cv.namedWindow("threshold", cv.WINDOW_NORMAL)

    cv.imshow("Source", src)
    # cv.imshow("Standard Hough Line Transform", cdst)
    cv.imshow("Probabilistic Line Transform", cdstP)
    cv.imshow("threshold", mask)

    cv.imwrite("2-HoughLinesP.png",cdstP)
    cv.imwrite("3-result.png",mask)

    mix = cv.add(src, mask)
    cv.namedWindow("mix", cv.WINDOW_NORMAL)
    cv.imshow("mix", mix)


    cv.waitKey()
    return 0

if __name__ == "__main__":
    main(sys.argv[1:])