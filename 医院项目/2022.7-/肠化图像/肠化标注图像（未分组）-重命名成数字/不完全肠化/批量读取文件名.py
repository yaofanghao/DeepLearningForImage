# 批量读取文件名（不带后缀）

import os

def saveList(pathName):
    for file_name in pathName:
        with open("jpg.txt", "a") as f:
            f.write(file_name.split(".")[0] + "\n")

def dirList(path_list):
    for i in range(0, len(path_list)):
        path = os.path.join(file_path, path_list[i])
    if os.path.isdir(path):
        saveList(os.listdir(path))



file_path = "./jpg"
path_list = os.listdir(file_path)  # os.listdir(file)会历遍文件夹内的文件并返回一个列表
print(path_list)
path_name = []  # 把文件列表写入save.txt中

dirList(path_list)
saveList(path_list)
