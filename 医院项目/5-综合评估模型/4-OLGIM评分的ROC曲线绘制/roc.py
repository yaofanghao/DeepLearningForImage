'''
Author: yao fanghao
Date: 2023-05-31 17:01:05
LastEditTime: 2023-05-31 17:06:07
LastEditors: yao fanghao
'''
import numpy as np
import pandas as pd          

excel_file = 'test.xlsx'     
df = pd.read_excel(excel_file)

df.drop(df.index[[0]])  # 删除第一行
P = df.iloc[:,[1,2,3]]  #第1到第3列
P = np.array(P)
print(P.shape)
# P

L = df.iloc[:,[5,6,7]]
L = np.array(L)
print(L.shape)
# L

# label矩阵
label = df.iloc[:,[8]]
label = np.array(label)
label = label.ravel()
print(label.shape)
# label

from sklearn.metrics import roc_curve,auc
import matplotlib.pyplot as plt
import matplotlib;matplotlib.rc("font",family='Microsoft YaHei')

colors = ['magenta','green','cyan'] # 设置三条ROC曲线的颜色
num_classes = ['0-1分','2分','3分']
for j in range(len(num_classes)): # 循环三次
    label_class = []
    score = []
    for i in label:
        if i == j:
            label_class.append(1)
        else:
            label_class.append(-1)
    score = [P[i,j] for i in range(P.shape[0])]
    fpr, tpr, threshold = roc_curve(label_class, score)
    auc_result = auc(fpr, tpr)
    plt.plot(fpr, tpr, 'x-', color=colors[j], label=num_classes[j] + ', AUC值为' + str('%.3f'%auc_result)) 
plt.legend();

for i in range(P.shape[0]):
    fpr, tpr, threshold = roc_curve(L.ravel(),P.ravel())
    auc_result = auc(fpr, tpr)
plt.plot(fpr, tpr, 'x-', color='red', label='微平均法, AUC值为' + str('%.3f'%auc_result)) 
plt.plot([0,1],[0,1],'--', color='black', label='45°参考线')
plt.title('ROC 外部 result')
plt.legend();plt.show()