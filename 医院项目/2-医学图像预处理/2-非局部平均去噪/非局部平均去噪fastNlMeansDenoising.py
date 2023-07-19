# 2023.3.8 有点效果
# 非局部平均去噪方法

from scipy.signal import wiener
import cv2
import numpy as np
import matplotlib.pyplot as plt

# 设置不同参数比较效果
def Denoising(img):
    dst = cv2.fastNlMeansDenoisingColored(img, None,
                                          h = 4, templateWindowSize=7,
                                          searchWindowSize=21)
    return dst

if __name__ == '__main__':
    img = cv2.imread("1.jpg")
    cv2.imshow("img", img)

    img_denoising = Denoising(img)
    cv2.imshow("img_denoising", img_denoising)
    cv2.imwrite("1_fastNlMeansDenoising.jpg", img_denoising)

    cv2.waitKey(0)
    cv2.destroyAllWindows()