clc;
%clear all;
close all;

%% detection
img_path = 'imgs/5.jpg';
img = imread(img_path);
thresh = graythresh(img);
I2 = im2bw(img, thresh);

T1 = 250; % 高一点
T2_abs = 200; % 高一点
T2_rel = 1.5; % 高一点
N_min = 1000; % 影响不大
T3 = 5; % 影响不大
specular_mask = SpecularDetectionArnold2010(img, T1, T2_abs, T2_rel, N_min, T3);
specular_mask = specular_mask & I2; % filter the background
figure;imshow(specular_mask);

%% inpainting
decay_win_size = 10;
decay_cof = 20;
inpainted_img = InpainttingArnold2010(specular_mask, img, decay_win_size, decay_cof);
figure;imshow(img);
figure;imshow(inpainted_img);
