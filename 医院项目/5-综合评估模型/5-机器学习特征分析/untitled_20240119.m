x = {'决策树', 'BP100', 'BP200', 'BP100-5layer', 'ResNet1','ResNet2'};
y1 = [79.70, 87.13, 88.12, 92.57, 94.06, 95.05];
y2 = [79.70, 87.13, 88.12, 94.00, 95.00, 95.05];
y3 = [79.70, 87.13, 88.12, 93.00, 94.06, 95.05];

color_first = '#3CB371';
color_second = '#FF7744';
color_third = '#003399';
msize = 7;

figure;
hold on;

plot(y1, '-o', 'Color', color_first, 'MarkerSize', msize, 'DisplayName', 'accuracy');
plot(y2, '-^', 'Color', color_second, 'MarkerSize', msize, 'DisplayName', 'precision');
plot(y3, '-*', 'Color', color_third, 'MarkerSize', msize, 'DisplayName', 'recall');

xticks(1:numel(x));
xticklabels(x);
xtickangle(0); % 添加这行代码，使x轴名称水平显示
ylim([60,100])
ylabel('性能指标(%)');
title('分类模型对比结果');

legend('准确率', '精确率', '召回率');
grid on;

hold off;
