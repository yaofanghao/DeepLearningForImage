x = -10:0.1:10; % x轴范围
y_relu = max(0, x); % ReLU函数
y_leakyrelu = max(0.1*x, x); % LeakyReLU函数

plot(x, y_relu, 'r-', 'LineWidth', 2); % 绘制ReLU曲线，蓝色实线
hold on; % 保持坐标系不变
plot(x, y_leakyrelu, 'b--', 'LineWidth', 2); % 绘制LeakyReLU曲线，红色虚线

legend('ReLU', 'LeakyReLU'); % 添加图例
xlabel('x'); % x轴标签
ylabel('y'); % y轴标签
title('ReLU 与 LeakyReLU 对比'); % 图标题
grid on; % 显示网格
