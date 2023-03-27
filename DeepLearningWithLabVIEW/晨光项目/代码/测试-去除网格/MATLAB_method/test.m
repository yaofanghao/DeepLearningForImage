% https://blog.csdn.net/Crystal_remember/article/details/117330680
close all;
clear all;
clc;

%%
I = imread('test3.bmp'); 
I = rgb2gray(I);
totMask = zeros(size(I)); % accumulate all single object masks to this one 
f = figure('CurrentCharacter','a'); 
imshow(I) 
 
FFT = fft2(I);
myangle = angle(FFT);             %相位谱(没有进行移位的)
FS = abs(fftshift(FFT));          % 移位，使低频成分集中到图像中心，并得到幅度谱
S = log(1+abs(FS));
figure,imshow(S,[]);
 
small=min(min(FS));
h = imfreehand(gca); setColor(h,'green'); 
position = wait(h); 
BW = createMask(h); 
totMask = totMask | BW; % add mask to global mask 
while double(get(f,'CurrentCharacter'))~=27 
    % ask user for another mask 
    h = imfreehand(gca); 
    if isempty(h) 
     % User pressed ESC, or something else went wrong 
     continue 
    end 
    setColor(h,'green'); 
    position = wait(h); 
    BW = createMask(h); 
    totMask = totMask | BW; % add mask to global mask 
    pause(.1) 
end 
% show the resulting mask 
% figure; imshow(totMask); title('multi-object mask'); 
 
cost3 = FS;
cost3(totMask == 1) = small ;
FS = cost3; 
 
resul_s  = ifftshift(FS);               % 将处理后的幅度图反移位，恢复到正常状态
result_f = resul_s.*cos(myangle) + resul_s.*sin(myangle).*1i;      % 幅度值和相位值重新进行结合，得到复数
result_image = abs(ifft2(result_f ));               % 进行傅里叶反变换，得到处理后的时域图像
result = im2uint8(mat2gray(result_image));       
figure,imshow(result);       %去除网纹成分后的图像

%------
BW = imbinarize(result,0.75); % 二值化分割
figure,imshow(BW);



