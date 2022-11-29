import os
import xml.etree.ElementTree as ET
import tqdm

#######################
# 修改内容区域：
# xml所在文件夹路径，修改这个即可
root_dir = r"E:\\MyGithub\\1\\1630\\Annotations"
#######################

def del_delete_eq_1(xml_path):
    # 从xml文件中读取，使用getroot()获取根节点，得到的是一个Element对象
    tree = ET.parse(xml_path)
    root = tree.getroot()
    for object in root.findall('object'):
        deleted = str(object.find('name').text)
        if (deleted in ['NEO', 'NONNEO']):
            root.remove(object)
            print(xml_path)
    tree.write(xml_path)

if __name__ == '__main__':
    xml_path_list = [os.path.join(root_dir, x) for x in os.listdir(root_dir)]
    for xml in tqdm.tqdm(xml_path_list):
        del_delete_eq_1(xml)
