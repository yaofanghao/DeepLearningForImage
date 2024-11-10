x = {'精细决策树', '核朴素贝叶斯', '二次SVM', '加权KNN', '集成RUS-Boosted树'};
y1 = [71.9, 73.8, 80.7, 84.6, 83.1];
y2 = [72.6, 74.5, 79.7, 89.8, 87.2];
y3 = [68.6, 72.5, 83.1, 86.1, 83.1];

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
title('模型对比结果');

legend('accuracy', 'precision', 'recall');
grid on;

hold off;
