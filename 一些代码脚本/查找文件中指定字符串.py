import os

path = "训练集2/肠化训练集"  #待搜索的目录路径
find = "."     #要查找的字符串
result = []    #保存结果的数组

def findfiles():
    count = 1

    # 查找文件名中的指定字符串（包含后缀中的字符串）
    # for root, dirs, files in os.walk(path):
    #     for filename in files:
    #         if "." in filename:
    #             result.append([count, root + "/" + filename])
    #             count += 1

    # 查找文件名中的指定字符串（不包含后缀中的字符串）
    for root, dirs, files in os.walk(path):
        for filename in files:
            stem, suffix = os.path.splitext(filename)
            if find in stem:
                result.append([count, root + "/" + filename])
                count += 1

    print("所查找的文件夹为：" + path)
    print("要查找的是：" + find + '\n')

    for i in range(len(result)):
        print(result[i])
        print('\n')

if __name__ == '__main__':
    findfiles()
