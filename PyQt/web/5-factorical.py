"""
用Python语言编写计算阶乘的类
"""
from PyQt5.QtCore import *

class Factorial(QObject):
    @pyqtSlot(int,result=int)
    def factorial(self,n):
        if n == 0 or n == 1:
            return 1
        else:
            return self.factorial(n-1)* n


