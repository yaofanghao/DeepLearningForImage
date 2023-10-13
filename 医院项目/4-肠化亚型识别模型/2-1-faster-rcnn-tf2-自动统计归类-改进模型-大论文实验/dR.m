% 损失函数的导数
function y = dR(x)
y = zeros(size(x));
y(x<-1) = -1;
y(x>1) = 1;
y(x>=-1 & x<=1) = x(x>=-1 & x<=1);
end