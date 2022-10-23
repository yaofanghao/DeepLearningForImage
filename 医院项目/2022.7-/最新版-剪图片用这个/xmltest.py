from lxml import etree

#-------------------------------#
# 生成xml的类 GEN_Annotations
# 参考资料：https://blog.csdn.net/u014090429/article/details/94613764
# 姚方浩 2022.6.21

class GEN_Annotations:
    def __init__(self, filename): # 类的基本属性，可根据需要使用或修改
        self.root = etree.Element("annotation")

        child1 = etree.SubElement(self.root, "folder")
        child1.text = "这个用不到"
        child2 = etree.SubElement(self.root, "filename")
        child2.text = filename
        child3 = etree.SubElement(self.root, "path")
        child3.text = "这个用不到"
        child4 = etree.SubElement(self.root, "source")
        child5 = etree.SubElement(child4, "database")
        child5.text = "Unknown"

    def set_size(self, witdh, height, channel):
        size = etree.SubElement(self.root, "size")
        widthn = etree.SubElement(size, "width")
        widthn.text = str(witdh)
        heightn = etree.SubElement(size, "height")
        heightn.text = str(height)
        channeln = etree.SubElement(size, "depth")
        channeln.text = str(channel)

    def add_pic_attr(self, label, xmin, ymin, xmax, ymax): # 设置标注框的信息
        segmented = etree.SubElement(self.root, "segmented")
        segmented.text = "0"
        object = etree.SubElement(self.root, "object")
        namen = etree.SubElement(object, "name")
        namen.text = label
        pose = etree.SubElement(object, "pose")
        pose.text = "Unspecified"
        truncated = etree.SubElement(object, "truncated")
        truncated.text = "0"
        difficult = etree.SubElement(object, "difficult")
        difficult.text = "0"

        bndbox = etree.SubElement(object, "bndbox")
        xminn = etree.SubElement(bndbox, "xmin")
        xminn.text = str(xmin)
        yminn = etree.SubElement(bndbox, "ymin")
        yminn.text = str(ymin)
        xmaxn = etree.SubElement(bndbox, "xmax")
        xmaxn.text = str(xmax)
        ymaxn = etree.SubElement(bndbox, "ymax")
        ymaxn.text = str(ymax)

    def savefile(self, filename): # 导出xml并美观格式
        tree = etree.ElementTree(self.root)
        tree.write(filename, pretty_print=True, xml_declaration=False, encoding='utf-8')

if __name__ == '__main__':
    filename = "000001.jpg" # 图片名
    anno = GEN_Annotations(filename)
    anno.set_size(621, 540, 3) # 图片尺寸
    xmin = 93    # 框的四个坐标值
    ymin = 260
    xmax = 247
    ymax = 407
    anno.add_pic_attr("NEO", xmin, ymin, xmax, ymax) #设置name的类别
    anno.savefile("00001.xml") #导出的xml文件名