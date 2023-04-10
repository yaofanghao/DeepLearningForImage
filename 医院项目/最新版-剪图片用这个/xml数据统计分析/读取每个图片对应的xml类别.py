import os
import xml.etree.ElementTree as ET
import tqdm

#######################
# xml所在文件夹路径，修改这个即可
root_dir = "./neibu-output/xml"
#######################

if __name__ == '__main__':
    xml_path_list = [os.path.join(root_dir, x) for x in os.listdir(root_dir)]
    f1 = open(os.path.join(os.getcwd(), 'xml_class.txt'), 'a')
    for xml_path in tqdm.tqdm(xml_path_list):
        tree = ET.parse(xml_path)
        root = tree.getroot()
        for object in root.findall('object'):
            deleted = str(object.find('name').text)
            # if (deleted in ['NEO', 'NONNEO']):
            #     root.remove(object)
            xml_info = str(xml_path) + ", predict result is " + deleted
            print(xml_info)
            f1.write(xml_info)
            f1.write("\r")
    
    f1.close()