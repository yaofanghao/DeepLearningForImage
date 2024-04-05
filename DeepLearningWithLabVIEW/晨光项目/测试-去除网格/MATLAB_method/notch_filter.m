clc;
clear;
close all;
f=imread('test.bmp');
f=rgb2gray(f);
figure;
subplot(2,2,1);imshow(f);title('原图');
%% 均衡化
h=zeros(256,1);
for k=0:255
    h(k+1)=sum(sum(f==k));
end
p=h/sum(h);
s=zeros(256,1);
s(1)=p(1);
for k=2:255
    s(k)=s(k-1)+p(k);
end
f=double(f);
[r,c]=size(f);
t=zeros(256,1);
t=double(t);
for m=1:r
    for n=1:c
        t(m,n)=s(f(m,n)+1);
    end
end
subplot(2,2,2);imshow(t);title('均衡化后的图像');
%% 频谱图
g=uint8(t*255);
s=fft2(g);
s_shift=fftshift(s);
subplot(2,2,3);
imshow(log(1+s_shift),[]);title('均衡化后频谱图');
%% 陷波滤波
H= zeros(size(g));
[w,h]=size(g);
%滤波器圆心
rx1 = w / 4;
ry1 = h / 2;
rx2 = w * 3 / 4;
ry2 = h / 2;
r = min(w,h)/5;%半径
for i = 1:w
    for j = 1:h
        if(i-rx1)^2+(j-ry1)^2 >= r*r && (i-rx2)^2+(j-ry2)^2 >= r*r
            H(i,j) = 1;
        end
    end
end
G=H.*s_shift;
g=ifft2(ifftshift(G),'symmetric');
g=uint8(real(g));
subplot(2,2,4);imshow(g);title('滤波变换图');
figure;imshow(H);
 
%% 中值滤波
t=t*255;
w=6;
fn=padarray(t,[w w],'symmetric');
[r,c]=size(fn);
g=zeros(r,c);
nc=ceil((2*w+1)/2);
for m=1+w:r-w
    for n=1+w:c-w
        roi=fn(m-w:m+w,n);
        p=sort(roi(:));
        g(m,n)=p(nc);
    end
end
g=g(1+w:r-w,1+w:c-w);
figure;
subplot(1,2,1);imshow(t,[]);
subplot(1,2,2);
imshow(g,[]);
title('中值滤波');
