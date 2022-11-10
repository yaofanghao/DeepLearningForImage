import os
from tqdm import tqdm
import xml.dom.minidom

# xml所在文件夹路径，修改这个即可
SrcDir = r"E:\\MyGithub\\1\\xml"


def ReadXml(FilePath):
    if os.path.exists(FilePath) is False:
        return None
    dom = xml.dom.minidom.parse(FilePath)
    root_ = dom.documentElement
    object_ = root_.getElementsByTagName('object')
    info = []
    for object_1 in object_:
        name = object_1.getElementsByTagName("name")[0].firstChild.data
        bndbox = object_1.getElementsByTagName("bndbox")[0]
        xmin = int(bndbox.getElementsByTagName("xmin")[0].firstChild.data)
        ymin = int(bndbox.getElementsByTagName("ymin")[0].firstChild.data)
        xmax = int(bndbox.getElementsByTagName("xmax")[0].firstChild.data)
        ymax = int(bndbox.getElementsByTagName("ymax")[0].firstChild.data)
        info.append([xmin, ymin, xmax, ymax, name])
    return info


def CountLabelKind(Path):
    LabelDict = {}
    print("Star to count label kinds....")
    for root, dirs, files in os.walk(Path):
        for file in tqdm(files):
            if file[-1] == 'l':
                Infos = ReadXml(root + "\\" + file)
                for Info in Infos:
                    if Info[-1] not in LabelDict.keys():
                        LabelDict[Info[-1]] = 1
                    else:
                        LabelDict[Info[-1]] += 1

    return dict(sorted(LabelDict.items(), key=lambda x: x[0]))


if __name__ == '__main__':
    LabelDict = CountLabelKind(SrcDir)
    KeyDict = sorted(LabelDict)
    print("%d kind labels and %d labels in total:" % (len(KeyDict), sum(LabelDict.values())))
    print(KeyDict)
    print("Label Name and it's number:")
    for key in KeyDict:
        print("%s\t: %d" % (key, LabelDict[key]))
