import os
from PIL import Image

count = os.listdir("E:\标注图\make——dataset\png1")
for i in range(0, len(count)):
    path = os.path.join("E:\标注图\make——dataset\png1", count[i])
    img_1 = Image.open(path)
    if img_1.size == (1276, 1020):
        print(count[i])
        # crop_box = (165, 35, img_1.size[0] - 5, img_1.size[1] - 25)
        # img_2 = img_1.crop(crop_box)
        # img_2.save(path)
        # print(1)