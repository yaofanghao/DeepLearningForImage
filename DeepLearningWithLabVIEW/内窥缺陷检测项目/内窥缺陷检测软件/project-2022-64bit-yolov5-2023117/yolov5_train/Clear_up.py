from PIL import Image
import os
import xml.etree.ElementTree as ET
import json
# 输入文件夹的路径
input_p = "./VOCdevkit/VOC2007/JPEGImages"
input_a ="./VOCdevkit/VOC2007/Annotations"
p_list = os.listdir(input_p)
a_list = os.listdir(input_a)

# 指定目录 用于json转xml
# ------------------------------------------------------#
json_directory = "./VOCdevkit/VOC2007/Json"
xml_directory = './VOCdevkit/VOC2007/Xml_new'
# 创建xml_out文件夹
if not os.path.exists(xml_directory):
    os.makedirs(xml_directory)
#-------------------------------------------------------#

#所有图片后缀转变为.jpg
def convert_images_to_jpg(input_folder):
    # 获取输入文件夹中的文件列表
    p_list = os.listdir(input_folder)

    # 循环遍历输入文件夹中的文件
    for filename in p_list:
        if filename.endswith(".png") or filename.endswith(".JPG"):
            file_path = os.path.join(input_folder, filename)

            # 打开图片
            with Image.open(file_path) as img:
                # 转换图像为RGB模式
                img = img.convert("RGB")

                # 构建输出文件路径，替换原始文件
                output_filename = os.path.splitext(filename)[0] + ".jpg"
                output_file_path = os.path.join(input_folder, output_filename)

                # 保存修改后的图片，替换原始文件
                img.save(output_file_path, "JPEG")

    print("图片替换完成！")

#删除图片和标签文件的空格
def remove_spaces_in_filenames(file_list, input_folder):
    for filename in file_list:
        # 构建原始文件的完整路径
        old_file_path = os.path.join(input_folder, filename)

        # 检查文件名中是否包含空格
        if " " in filename:
            # 删除文件名中的空格
            new_filename = filename.replace(" ", "")
            # 构建新文件的完整路径
            new_file_path = os.path.join(input_folder, new_filename)
            # 重命名文件
            os.rename(old_file_path, new_file_path)
            print(f"已重命名文件: {filename} -> {new_filename}")

    print("空格删除完成！")

#标签里的duoyvwu变为duoyuwu
def modify_xml_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):
            file_path = os.path.join(folder_path, filename)
            tree = ET.parse(file_path)
            root = tree.getroot()

            for name_elem in root.iter("name"):
                if name_elem.text == "duoyvwu":
                    name_elem.text = "duoyuwu"

            tree.write(file_path)

def convert_json_to_xml(input_file, output_file):
    # 读取JSON文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 创建根节点
    root = ET.Element('annotation')

    # 添加图片路径节点
    filename = ET.SubElement(root, 'filename')
    filename.text = str(data['imagePath'])

    # 添加目标节点
    for shape in data['shapes']:
        # 创建目标节点
        object_node = ET.SubElement(root, 'object')

        # 添加目标类别节点
        label = ET.SubElement(object_node, 'name')
        label.text = str(shape['label'])

        # 添加边界框节点
        bndbox = ET.SubElement(object_node, 'bndbox')

        # 解析坐标信息
        points = shape['points']
        x_coords = [int(point[0]) for point in points]
        y_coords = [int(point[1]) for point in points]
        xmin = min(x_coords)
        ymin = min(y_coords)
        xmax = max(x_coords)
        ymax = max(y_coords)

        # 添加坐标节点
        xmin_node = ET.SubElement(bndbox, 'xmin')
        xmin_node.text = str(xmin)

        ymin_node = ET.SubElement(bndbox, 'ymin')
        ymin_node.text = str(ymin)

        xmax_node = ET.SubElement(bndbox, 'xmax')
        xmax_node.text = str(xmax)

        ymax_node = ET.SubElement(bndbox, 'ymax')
        ymax_node.text = str(ymax)

    # 创建XML树
    tree = ET.ElementTree(root)

    # 保存为XML文件
    tree.write(output_file)

def convert_all_json_files_to_xml(input_directory, output_directory):
    # 查找并处理所有的JSON文件
    for file in os.listdir(input_directory):
        if file.endswith('.json'):
            json_file = os.path.join(input_directory, file)
            xml_file = os.path.join(output_directory, os.path.splitext(file)[0] + '.xml')
            convert_json_to_xml(json_file, xml_file)
            print(file + ' 转换成功')





convert_images_to_jpg(input_p)

remove_spaces_in_filenames(p_list, input_p)

remove_spaces_in_filenames(a_list, input_a)

# 调用函数进行修改
modify_xml_files(input_a)

# 调用函数
# convert_all_json_files_to_xml(json_directory, xml_directory)

