% 改进的损失函数smoothl1plus
x = -2:0.1:2;
y = 1/log(2)*((abs(x)+1).*log(abs(x)+1)+log(2)-abs(x));   
plot(x,y);

% 改进的损失函数的导数
x1 = -1:0.1:1;
x2 = -1:0.1:1;
y1 = log(x+1)/log(2);
y2 = -log(-x+1)/log(2);
plot(x1,y1);
hold on;
plot(x2,y2)
