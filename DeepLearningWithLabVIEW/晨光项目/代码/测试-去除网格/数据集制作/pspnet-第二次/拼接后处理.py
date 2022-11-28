# https://docs.opencv.org/4.x/d9/db0/tutorial_hough_lines.html

import sys
import math
import cv2 as cv
import numpy as np

def main(argv):
    default_file = '0-source.jpg'
    predict_file = '1-predict.jpg'
    src0 = cv.imread(default_file, cv.IMREAD_GRAYSCALE)
    src = np.copy(src0)
    mask = cv.imread(predict_file, cv.IMREAD_GRAYSCALE)

    cv.imshow("before dilate", mask)

    # 对mask做一点膨胀
    mask = cv.dilate(mask,kernel=np.ones((5,5),np.uint8))
    cv.imshow("after dilate", mask)
    cv.imwrite("1-1predict_dilate.jpg", mask)

    mask_inv = cv.bitwise_not(mask)
    cv.imwrite("2-predict_inv.jpg", mask_inv)

    # dst = cv.Canny(src0, 0, 150, None, 3)
    # # cv.imshow("canny", dst)

    # 对霍夫P变换检测到的线作为二次判断条件
    # print(cdstP[0,0,0])
    # print(cdstP.shape)
    # print(cdstP[1256,1257])
    # print(cdstP[1256,1257][2])
    for i in range(src.shape[0]):
        for j in range(src.shape[1]):
            # 对深度学习预测得到的图片中的白色部分排除为缺陷的可能，设置为白色
            # flag1 = (mask[i, j][0] == 255) & (mask[i, j][1] == 255) & (mask[i, j][2] == 255)
            flag1 = (mask[i, j] > 250)
            if flag1:
                src[i, j] = 255
            else:
                pass

    # 阈值分割
    # 150以上的设为全黑
    ret, mask = cv.threshold(src, 100, 255, 0) #简单二值化

    cv.namedWindow("Preprocess", cv.WINDOW_NORMAL)
    cv.imshow("Preprocess", src)
    cv.imwrite("3-final-output.jpg", src)
    cv.imwrite("4-mask.png",mask)

    cv.waitKey()
    return 0

if __name__ == "__main__":
    main(sys.argv[1:])