%损失函数R
function y = R(x)
y = zeros(size(x));
y(x<-1) = -x(x<-1)-0.5;
y(x>1) = x(x>1)-0.5;
y(x>=-1 & x<=1) = 0.5*x(x>=-1 & x<=1).^2;
end