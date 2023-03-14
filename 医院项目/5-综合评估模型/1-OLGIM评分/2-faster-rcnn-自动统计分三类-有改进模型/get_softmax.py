import numpy
def softmax(x):
    x = numpy.where(x==0, -5, x)  # 0的时候，视为一个极小的值exp计算为一个很小的值
    row_max = numpy.max(x)
    # 每行元素都需要减去对应的最大值，否则求exp(x)会溢出，导致inf情况
    x = x - row_max
    x_exp = numpy.exp(x)
    x_sum = numpy.sum(x_exp)
    s = x_exp / x_sum
    s = numpy.around(s, 4)
    return s

# x = [0.75, 0.4, 0.1]
x = numpy.array ([1.0, 0, 0])

y = softmax(x)
print(y)