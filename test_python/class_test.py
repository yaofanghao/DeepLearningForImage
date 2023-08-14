"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/7/12 17:06
    @Filename: class_test.py
    @Software: PyCharm     
"""

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.__Parameter = age

    # 2023.7.12 装饰器
    def GetValue(self):
        return self.__Parameter

    def say_hello(self):
        print(f"Hello, my name is {self.name} and I'm {self.age} years old.")


# 2023.7.12-重写
# 包装函数
def getClassData():
    newClassObject = Person("Alice", 25)
    return newClassObject.GetValue()


# 创建Person对象
# person = Person("Alice", 25)

# 调用对象的方法
# person.say_hello()

returnValue = getClassData()
print(returnValue)