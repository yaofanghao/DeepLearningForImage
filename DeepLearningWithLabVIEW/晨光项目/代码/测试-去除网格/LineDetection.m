% 线检测模板 
% https://www.docin.com/p-1527386962.html
close all;
clear all;
clc;

%%
%线检测测试图像（Detection of Line）
I=im2double(imread('test.bmp'));
I = rgb2gray(I);
[M,N]=size(I);

% 腐蚀
% se = strel('square',5);
% se2 = strel('line',10,90);
% Ierode = imerode(I, se);
% Ierdoe = imerode(Ierode, se2);
% figure,imshow(Ierode);

% I = medfilt2(I,[3 3]);   % 采用二维中值滤波函数对图像滤波，滤波窗口是3*3
% guas_fit = medfilt2(guas_img,[3,3]);  % 滤除高斯噪声


%===============================线检测(二)=================================
%线检测方向算子
L_Horizontal=[-1 -1 -1;2 2 2;-1 -1 -1];
L_45=[2 -1 -1;-1 2 -1;-1 -1 2;];
L_Vertical=[-1 2 -1;-1 2 -1;-1 2 -1];
L_135=[-1 -1 2;-1 2 -1 ;2 -1 -1];
%上述方向算子的大小
n=3;
g_Horizontal=zeros(M,N);
g_45=zeros(M,N);
g_Vertical=zeros(M,N);
g_135=zeros(M,N);
n_l=floor(n/2);
%对原图进行扩展，方便处理边界
I_pad=padarray(I, [n_l,n_l],'symmetric');

% 根据需要自行调整的阈值
T=0.5;
for i=1:M
    for j=1:N
        %获得图像子块区域
        Block=I_pad(i:i+2*n_l,j:j+2*n_l);
        %用拉氏内核对子区域卷积
        g_Horizontal(i,j)=sum(sum(-L_Horizontal.*Block)); 
        g_Vertical(i,j)=sum(sum(-L_Vertical.*Block)); 
    end
end
% figure,imshow(g_Horizontal);
% figure,imshow(g_Vertical);

% 水平和垂直叠加
g_mix = g_Horizontal | g_Vertical;
figure,imshow(g_mix);


