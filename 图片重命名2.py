import os

path = 'jpg/'
path1 = 'jpg2/'
filelist = os.listdir(path)

# 图片名先转化为int后分类（sort）
# 按顺序读取图片，这样保证是1,2,3...而不是1,10,11...
filelist.sort(key=lambda x: int(x.split('.')[0]))

i = 1
for item in filelist:

    if item.endswith('.jpg'):
        src = os.path.join(path, item)   #原名位置
        s = str(i)
        # s = s.zfill(6)     #右对齐名称,这里不用
        dst = os.path.join(path1, 'image' + s + '.jpg')  #改名后位置
        os.rename(src, dst)  #重命名
        print ('convert %s to %s ...' % (src, dst))
        i = i + 1
    print('success')
