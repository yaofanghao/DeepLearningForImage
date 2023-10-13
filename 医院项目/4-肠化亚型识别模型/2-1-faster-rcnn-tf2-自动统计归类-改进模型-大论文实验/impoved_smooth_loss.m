%% 原始损失函数R 图象
x = -5:0.1:5;
y3 = R(x);
plot(x,y3, 'r-', 'LineWidth', 2);
hold on;
xlim([-5, 5]); 
ylim([-2, 5]); 

% 损失函数的导数
y4 = dR(x);
plot(x,y4, 'b-', 'LineWidth', 2);

legend('R', 'dR'); 
xlabel('x'); 
ylabel('y'); 
title('R vs dR'); 
grid on;

%% 改进的损失函数smoothl1plus
x = -3:0.1:3;
y = 1/log(2)*((abs(x)+1).*log(abs(x)+1)+log(2)-abs(x));   
plot(x,y, 'r-', 'LineWidth', 2);
hold on;

% 改进的损失函数的导数
y2 = dQ(x);
plot(x,y2, 'b-', 'LineWidth', 2);

% legend('Q', 'dQ'); 
% xlabel('x'); 
% ylabel('y'); 
% title('Q vs dQ'); 
grid on;

legend('R', 'dR', 'Q', 'dQ'); 
xlabel('x'); 
ylabel('y'); 
title('损失函数及其导数对比'); 
grid on;
