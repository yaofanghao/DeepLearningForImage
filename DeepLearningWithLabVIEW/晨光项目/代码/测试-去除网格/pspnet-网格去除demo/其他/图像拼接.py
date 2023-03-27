# 2022.10.11 图像拼接代码
# 8x30

import PIL.Image as Image
import os

#-------------设置区域-----------------
IMAGES_PATH = './img_out/'  # 图片集地址
IMAGES_FORMAT = ['.jpg', '.JPG','.png']  # 图片格式
IMAGE_W = 178
IMAGE_H = 146
IMAGE_ROW = 8  # 合并成一张图后，一共有几行
IMAGE_COLUMN = 30  # 合并成一张图后，一共有几列
IMAGE_SAVE_PATH = '1-predict.jpg'  # 图片拼接后保存的地址
padding=0
head_padding=0
#-------------设置区域-----------------

# 获取图片集地址下的所有图片名称
image_names = [name for name in os.listdir(IMAGES_PATH) for item in IMAGES_FORMAT if
               os.path.splitext(name)[1] == item]

# 按数字排序
image_names.sort(key=lambda x: int(x[:-4]))

# 判断有效性
if len(image_names) != IMAGE_ROW * IMAGE_COLUMN:
    raise ValueError("合成图片的参数和要求的数量不能匹配！")

# 拼接函数
def image_compose():
    to_image = Image.new('RGB',(IMAGE_COLUMN * IMAGE_W+padding*(IMAGE_COLUMN-1), head_padding+IMAGE_ROW * IMAGE_H+padding*(IMAGE_ROW-1)),'white' )  # 创建一个新图
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    for y in range(1, IMAGE_ROW + 1):
        for x in range(1, IMAGE_COLUMN + 1):
            from_image = Image.open(IMAGES_PATH + image_names[IMAGE_COLUMN * (y - 1) + x - 1]).resize(
                (IMAGE_W, IMAGE_H), Image.ANTIALIAS)
            to_image.paste(from_image, ((x - 1) * IMAGE_W+padding* (x - 1), head_padding+(y - 1) * IMAGE_H+padding* (y - 1)))

    return to_image.save(IMAGE_SAVE_PATH)  # 保存

if __name__ == "__main__":
    image_compose()
