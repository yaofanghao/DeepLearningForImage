import os
names = os.listdir('C:\\Users\\姚方浩\\Desktop\\训练集\\肿瘤性2\\JPEGImages')
i=0
train_val = open('test2.txt','w')
for name in names:
    index = name.rfind('.')
    name = name[:index]
    train_val.write(name+'\n')
    i=i+1
    print(i)