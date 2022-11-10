# 2022.11.10 @ yaofanghao
import os
import shutil
import xml.etree.ElementTree as ET
import tqdm

# 针对OLGIM四分类问题，将测试集按照四种标签分类至四个文件夹
# 修改以下三项
root_dir = "E:\MyGithub\\1"  # 根目录
origin_xml_dir = str(root_dir) + "\\xml" #根目录下存放所有标签的xml文件
origin_jpg_dir = str(root_dir) + "\\jpg" #根目录下存放所有标签的jpg文件

class0_dir = str(root_dir) + "\\xml0\\"
class0_jpg_dir = str(root_dir) + "\\jpg0\\"
class1_dir = str(root_dir) + "\\xml1\\"
class1_jpg_dir = str(root_dir) + "\\jpg1\\"
class2_dir = str(root_dir) + "\\xml2\\"
class2_jpg_dir = str(root_dir) + "\\jpg2\\"
class3_dir = str(root_dir) + "\\xml3\\"
class3_jpg_dir = str(root_dir) + "\\jpg3\\"
if not os.path.exists(class1_dir):
    os.makedirs(class1_dir)
if not os.path.exists(class0_dir):
    os.makedirs(class0_dir)
if not os.path.exists(class0_jpg_dir):
    os.makedirs(class0_jpg_dir)
if not os.path.exists(class1_jpg_dir):
    os.makedirs(class1_jpg_dir)
if not os.path.exists(class2_dir):
    os.makedirs(class2_dir)
if not os.path.exists(class2_jpg_dir):
    os.makedirs(class2_jpg_dir)
if not os.path.exists(class3_dir):
    os.makedirs(class3_dir)
if not os.path.exists(class3_jpg_dir):
    os.makedirs(class3_jpg_dir)


if __name__ == '__main__':
    xml_path_list = [os.path.join(origin_xml_dir, x) for x in os.listdir(origin_xml_dir)]
    jpg_path_list = [os.path.join(origin_jpg_dir, x) for x in os.listdir(origin_jpg_dir)]
    flag = 0
    for xml_path in tqdm.tqdm(xml_path_list):
        # 从xml文件中读取，使用getroot()获取根节点，得到的是一个Element对象
        tree = ET.parse(xml_path)
        root = tree.getroot()
        for object in root.findall('object'):
            xml_name = str(object.find('name').text)
            if xml_name == '0分':
                root.remove(object)
                fpath, fname = os.path.split(xml_path_list[flag])
                fpath1, fname1 = os.path.split(jpg_path_list[flag])
                shutil.copy(xml_path_list[flag], class0_dir+fname)
                shutil.copy(jpg_path_list[flag], class0_jpg_dir+fname1)
                print("0分 | copy %s -> %s"%(xml_path_list[flag], class0_dir+fname))
                print("0分 | copy %s -> %s"%(jpg_path_list[flag], class0_jpg_dir+fname1))
                print("------------------")
                flag += 1
            if xml_name == '1分':
                root.remove(object)
                fpath, fname = os.path.split(xml_path_list[flag])
                fpath1, fname1 = os.path.split(jpg_path_list[flag])
                shutil.copy(xml_path_list[flag], class1_dir+fname)
                shutil.copy(jpg_path_list[flag], class1_jpg_dir+fname1)
                print("1分 | copy %s -> %s"%(xml_path_list[flag], class1_dir+fname))
                print("1分 | copy %s -> %s"%(jpg_path_list[flag], class1_jpg_dir+fname1))
                print("------------------")
                flag += 1
            if xml_name == '2分':
                root.remove(object)
                fpath, fname = os.path.split(xml_path_list[flag])
                fpath1, fname1 = os.path.split(jpg_path_list[flag])
                shutil.copy(xml_path_list[flag], class2_dir+fname)
                shutil.copy(jpg_path_list[flag], class2_jpg_dir+fname1)
                print("2分 | copy %s -> %s"%(xml_path_list[flag], class2_dir+fname))
                print("2分 | copy %s -> %s"%(jpg_path_list[flag], class2_jpg_dir+fname1))
                print("------------------")
                flag += 1
            if xml_name == '3分':
                root.remove(object)
                fpath, fname = os.path.split(xml_path_list[flag])
                fpath1, fname1 = os.path.split(jpg_path_list[flag])
                shutil.copy(xml_path_list[flag], class3_dir+fname)
                shutil.copy(jpg_path_list[flag], class3_jpg_dir+fname1)
                print("3分 | copy %s -> %s"%(xml_path_list[flag], class3_dir+fname))
                print("3分 | copy %s -> %s"%(jpg_path_list[flag], class3_jpg_dir+fname1))
                print("------------------")
                flag += 1
            # else:
            #     flag +=1
    print("图片总数：" + str(flag) + "success")
