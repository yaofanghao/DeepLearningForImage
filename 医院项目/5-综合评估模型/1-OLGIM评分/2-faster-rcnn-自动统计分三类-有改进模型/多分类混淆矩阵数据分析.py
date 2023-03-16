# https://zhuanlan.zhihu.com/p/216642469
import numpy as np

def cal_metrics(confusion_matrix):
    n_classes = confusion_matrix.shape[0]
    metrics_result = []
    for i in range(n_classes):
        # 逐步获取 真阳，假阳，真阴，假阴四个指标，并计算三个参数
        ALL = np.sum(confusion_matrix)
        # 对角线上是正确预测的
        TP = confusion_matrix[i, i]
        # 列加和减去正确预测是该类的假阳
        FP = np.sum(confusion_matrix[:, i]) - TP
        # 行加和减去正确预测是该类的假阴
        FN = np.sum(confusion_matrix[i, :]) - TP
        # 全部减去前面三个就是真阴
        TN = ALL - TP - FP - FN
        metrics_result.append([round(FP/(FP+TN), 4), round(TP/(TP+FN), 4)]) # 灵敏度 和 1-特异度
    return metrics_result

confusion_matrix = np.array([[90, 6, 4],[15, 150, 4],[6, 7, 50]])
print(cal_metrics(confusion_matrix))