import cv2   

def func():

    img = cv2.imread("1.jpg")
    cv2.namedWindow("Image")
    cv2.imshow("Image", img)
    cv2.waitKey (0)
    cv2.destroyAllWindows()

    return 1

func()