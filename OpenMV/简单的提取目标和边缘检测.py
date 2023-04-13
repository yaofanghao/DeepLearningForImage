# 2023.4.13 update
import sensor, image, time

sensor.reset()
sensor.set_framesize(sensor.QQVGA)
sensor.set_pixformat(sensor.RGB565)
sensor.skip_frames(time = 2000)

#设置颜色阈值，如果是rgb图像，六个数字分别为(minL, maxL, minA, maxA, minB, maxB)；
#如果是灰度图，则只需设置（min, max）两个数字即可。
threshold = (38,100,-20,127,15,127)# L A B 8, 55, -128, 112, 117, -120

# 在OV7725 sensor上, 边缘检测可以通过设置sharpness/edge寄存器来增强。
# 注意:这将在以后作为一个函数实现
if (sensor.get_id() == sensor.OV7725):
    sensor.__write_reg(0xAC, 0xDF)
    sensor.__write_reg(0x8F, 0xFF)

while(True):
    img = sensor.snapshot()  # 原图
    img2 = img.copy() # 原图拷贝

    # mask是二值化后的掩膜图像 将在thresholds内的图像部分像素变为1白，阈值外的部分变为0黑
    mask = img.binary([threshold])

    # mask和原图拷贝做逻辑与运算，得到目标区域，非目标区域全黑
    img.b_and(img2,mask)

    # 转换为灰度图，再对目标区域进行边缘检测
    img = img.to_grayscale()
    img.find_edges(image.EDGE_SIMPLE, threshold=(50, 255))
