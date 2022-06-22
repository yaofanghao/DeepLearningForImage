import matplotlib.pyplot as plt

filename1 = 'epoch_loss_2021_12_14_01_16_54.txt'
filename2 = 'epoch_val_loss_2021_12_14_01_16_54.txt'

X, loss, val_loss = [], [], []
with open(filename1, 'r') as f:
    lines1 = f.readlines()

with open(filename2, 'r') as f:
    lines2 = f.readlines()

for i in range(2, len(lines1)): #前两个epoch的值太大,因此从第三个开始，视情况调整
    X.append(i)
    loss.append(float("{:.2f}".format(float(lines1[i]))))
    val_loss.append(float("{:.2f}".format(float(lines2[i]))))
    #注意要转化成浮点，否则是str格式，画出的图会有问题

# print(X)
# print(loss)
# print(val_loss)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

ax.plot(X, loss, 'k.', label='loss')
ax.plot(X, val_loss, 'k-', label='val_loss')
plt.xlim(-1, len(lines1))
# plt.ylim(0,100)
ax.legend() #自动生成图例
#plt.savefig('loss.png') #savefig要写在show前，否则显示空白
plt.show()
