% 
filename = 'all.xlsx';
sheet = 1; % Excel表格的工作表编号
range = 'A:K'; % 数据范围
[data, ~] = xlsread(filename, sheet, range);


x = data(:, 4);
y = data(:, 11);
z = data(:, 3);
categories = data(:, 6); % 类别

figure;
hold on;

unique_categories = unique(categories);
colors = ['r', 'g', 'b']; 
marker_size = 20;
for i = 1:numel(unique_categories)
    category = unique_categories(i);
    indices = find(categories == category);
    scatter3(x(indices), y(indices), z(indices), marker_size, colors(i), 'filled');
end


xlabel('能量');
ylabel('相关性');
zlabel('Z');
legend('0-1分', '2分', '3分');
title('图像特征值 能量-相关性关系');
hold off;

%% 绘制三维图像
filename = 'all.xlsx';
sheet = 1; % Excel表格的工作表编号
range = 'A:F'; % 数据范围
[data, ~] = xlsread(filename, sheet, range);

x = data(:, 1);
y = data(:, 2);
z = data(:, 3);
categories = data(:, 6); % 类别

figure;
hold on;

unique_categories = unique(categories);
colors = ['r', 'g', 'b']; 
marker_size = 20;
for i = 1:numel(unique_categories)
    category = unique_categories(i);
    indices = find(categories == category);
    scatter3(x(indices), y(indices), z(indices), marker_size, colors(i), 'filled');
end

xlabel('熵')
ylabel('能量');
zlabel('相关性');
legend('0-1分', '2分', '3分');
title('图像特征值 能量-相关性关系');
hold off;


