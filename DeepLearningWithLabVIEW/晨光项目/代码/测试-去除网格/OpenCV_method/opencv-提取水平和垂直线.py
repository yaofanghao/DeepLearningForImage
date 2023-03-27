# https://raw.githubusercontent.com/opencv/opencv/4.x/samples/python/tutorial_code/imgProc/morph_lines_detection/morph_lines_detection.py

"""
@file morph_lines_detection.py
@brief Use morphology transformations for extracting horizontal and vertical lines sample code
"""
import numpy as np
import sys
import cv2 as cv

def show_wait_destroy(winname, img):
    cv.imshow(winname, img)
    cv.moveWindow(winname, 500, 0)
    cv.waitKey(0)
    cv.destroyWindow(winname)

def main(argv):
    # if len(argv) < 1:
    #     print ('Not enough parameters')
    #     print ('Usage:\nmorph_lines_detection.py < path_to_image >')
    #     return -1

    # src = cv.imread(argv[0], cv.IMREAD_COLOR)
    src = cv.imread("test.bmp", cv.IMREAD_GRAYSCALE)

    if src is None:
        print ('Error opening image: ' + argv[0])
        return -1
    # cv.imshow("src", src)

    if len(src.shape) != 2:
        gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    else:
        gray = src
    # show_wait_destroy("gray", gray)

    #简单二值化
    gray = cv.bitwise_not(gray)
    bw = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, \
                                cv.THRESH_BINARY, 15, -2)
    # _, bw = cv.threshold(src, 100, 255, 1)
    # show_wait_destroy("binary", bw)

    # Create the images that will use to extract the horizontal and vertical lines
    horizontal = np.copy(bw)
    vertical = np.copy(bw)

    # 水平线检测
    # Specify size on horizontal axis
    cols = horizontal.shape[1]
    horizontal_size = cols // 30
    # Create structure element for extracting horizontal lines through morphology operations
    horizontalStructure = cv.getStructuringElement(cv.MORPH_RECT, (horizontal_size, 1))

    horizontal = cv.erode(horizontal, horizontalStructure)
    horizontal = cv.dilate(horizontal, horizontalStructure)

    show_wait_destroy("horizontal", horizontal)

    # 垂直线检测
    # Specify size on vertical axis
    rows = vertical.shape[0]
    verticalsize = rows // 30
    # Create structure element for extracting vertical lines through morphology operations
    verticalStructure = cv.getStructuringElement(cv.MORPH_RECT, (1, verticalsize))

    vertical = cv.erode(vertical, verticalStructure)
    vertical = cv.dilate(vertical, verticalStructure)

    show_wait_destroy("vertical", vertical)

    # Inverse vertical image
    # vertical = cv.bitwise_not(vertical)
    # show_wait_destroy("vertical_bit", vertical)

    # 叠加
    mix = cv.bitwise_or(horizontal, vertical)
    show_wait_destroy("mix", mix)

    # '''
    # Extract edges and smooth image according to the logic
    # 1. extract edges
    # 2. dilate(edges)
    # 3. src.copyTo(smooth)
    # 4. blur smooth img
    # 5. smooth.copyTo(src, edges)
    # '''
    #
    # # Step 1
    # edges = cv.adaptiveThreshold(vertical, 255, cv.ADAPTIVE_THRESH_MEAN_C, \
    #                             cv.THRESH_BINARY, 3, -2)
    # show_wait_destroy("edges", edges)
    #
    # # Step 2
    # kernel = np.ones((2, 2), np.uint8)
    # edges = cv.dilate(edges, kernel)
    # show_wait_destroy("dilate", edges)
    #
    # # Step 3
    # smooth = np.copy(vertical)
    #
    # # Step 4
    # smooth = cv.blur(smooth, (2, 2))
    #
    # # Step 5
    # (rows, cols) = np.where(edges != 0)
    # vertical[rows, cols] = smooth[rows, cols]
    #
    # # Show final result
    # show_wait_destroy("smooth - final", vertical)

    return 0

if __name__ == "__main__":
    main(sys.argv[1:])