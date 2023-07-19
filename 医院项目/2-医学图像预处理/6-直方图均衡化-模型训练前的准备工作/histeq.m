% https://blog.csdn.net/weixin_46803857/article/details/122047870

%% 彩色图像的直方图均衡化
clc; 
RGB=imread('1.jpg'); %输入彩色图像，得到三维数组
R=RGB(:,:,1); %分别取三维数组的一维，得到红绿蓝三个分量
G=RGB(:,:,2); %为 R G B。
B=RGB(:,:,3); 
subplot(4,2,1),imshow(RGB); %绘制各分量的图像及其直方图
title('原始真彩色图像 '); % 
subplot(4,2,3),imshow(R); 
title('真彩色图像的红色分量 '); 
subplot(4,2,4), imhist(R); 
title('真彩色图像的红色分量直方图 '); 
subplot(4,2,5),imshow(G); 
title('真彩色图像的绿色分量 '); 
subplot(4,2,6), imhist(G); 
title('真彩色图像的绿色分量直方图 '); 
subplot(4,2,7),imshow(B); 
title('真彩色图像的蓝色分量 '); 
subplot(4,2,8), imhist(B); 
title('真彩色图像的蓝色分量直方图 '); 
r=histeq(R); %对个分量直方图均衡化，得到个分量均衡化图像
g=histeq(G); 
b=histeq(B); 
figure, 
subplot(3,2,1),imshow(r); 
title('红色分量均衡化后图像 '); 
subplot(3,2,2), imhist(r); 
title('红色分量均衡化后图像直方图 '); 
subplot(3,2,3),imshow(g); 
title('绿色分量均衡化后图像 '); 
subplot(3,2,4), imhist(g); 
title('绿色分量均衡化后图像直方图 '); 
subplot(3,2,5), imshow(b); 
title('蓝色分量均衡化后图像 '); 
subplot(3,2,6), imhist(b); 
title('蓝色分量均衡化后图像直方图 '); 
figure, %通过均衡化后的图像还原输出原图像
newimg = cat(3,r,g,b); % 
imshow(newimg,[]); 
title('均衡化后分量图像还原输出原图 ');