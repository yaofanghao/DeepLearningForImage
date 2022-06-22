import shutil
import os
import pandas as pd

base_dir1 = './jpg' #要整理的jpg图位置
base_dir2 = './png' #要整理的png图位置
txt_dir = 'shaixuan_name.txt' #从jpg和png中移除此txt中的图片
output_dir = './fail/' #移除不要的jpg和png存放至此

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

list = pd.read_csv(txt_dir,sep='\s+',
                   names=['image_name'])
list.index +=1
# print(list.iloc[0,0])

file_object = open(txt_dir)
try:
    i = 0
    for line in file_object:
        # print(line)
        shutil.move(base_dir1+'/'+str(list.iloc[i,0])+'.jpg', output_dir)
        shutil.move(base_dir2+'/'+str(list.iloc[i,0])+'.png', output_dir)
        print(list.iloc[i, 0])

        i += 1

    print('共移除超出占比的图片数：')
    print(i)

finally:
    file_object.close()
