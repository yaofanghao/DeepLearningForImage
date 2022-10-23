import os

from PIL import Image
import math
import operator
import matplotlib.pyplot as plt
from functools import reduce

flag = "jpg"
# flag = "png"

if flag == "jpg":
    json_file = './jpg'
    alist = os.listdir(json_file)

    alist.sort(key=lambda x: int(x.split('.')[0]))

    for i in range(0, len(alist)):
        path = os.path.join(json_file, alist[i])
        im2 = Image.open(path)
        im2 = im2.rotate(175) #每次翻转后修改
        # im2.save(os.path.join("./jpgfz", alist[i]))
        save_path = "./jpgxz/" + str(i+1) + ".jpg"  #每次翻转后修改名称
        im2.save(save_path)
        print(i+1)

if flag == "png":
    json_file = './png'
    alist = os.listdir(json_file)

    alist.sort(key=lambda x: int(x.split('.')[0]))

    for i in range(0, len(alist)):
        path = os.path.join(json_file, alist[i])
        im2 = Image.open(path)
        im2 = im2.rotate(175)
        save_path = "./pngxz/" + str(i+1) + ".png"
        im2.save(save_path)
        print(i+1)

