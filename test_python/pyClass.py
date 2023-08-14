"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/7/13 15:17
    @Filename: pyClass.py
    @Software: PyCharm     
"""

class IncrementClass:
    def __init__(self, i):
        self.i = i
    def increment(self, a):
        res = a + self.i
        return res

def NumberForIncrement(obj, a):
    s = obj.increment(a)
    return s

def ObjInitialize(i):
    obj = IncrementClass(i)
    return obj