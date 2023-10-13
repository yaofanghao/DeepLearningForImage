% 改进的损失函数的导数
function y = dQ(x)
y = zeros(size(x));
y(x<0) = -log(-x(x<0)+1)/log(2);
y(x>=0 & x<inf) = log(x(x>=0 & x<inf)+1)/log(2);
end