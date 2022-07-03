# 屏幕坐标系
# 它是以屏幕左上角为原点，划分的坐标系

# 下面演示用面向过程的方式进行演示  （面向对象的方式需要创建类，创建方法）

import sys
from PyQt5.QtWidgets import QHBoxLayout,QMainWindow,QApplication,QPushButton,QWidget

# 创建实例
app = QApplication(sys.argv)
# 创建窗口
widget = QWidget()
# 在窗口里放button
btn = QPushButton(widget)
# 在button里面更改文本
btn.setText("按钮")

# 添加点击事件，让鼠标点击button后，打印出“onclick”
def onClick_Button():
    print("第一种方式获取各个值")
    # 窗口离屏幕原点到y轴的距离
    print("widget.x() = %d" % widget.x())   # 600 （以屏幕为原点的窗口横坐标）
    # 窗口离屏幕原点到x轴的距离
    print("widget.y() = %d" % widget.y())    # 200  （以屏幕为原点的窗口纵坐标，不包含标题栏）
    # 窗口本身的宽度
    print("widget.width()=%d" % widget.width())    # 300 (窗口宽度)
    # 窗口本身的高度
    print("widget.height()= %d" % widget.height())    # 240  (工作区高度)

    print("第二种方式获取各个值")
    # 窗口离屏幕原点到y轴的距离
    print("widget.geometry().x() = %d" % widget.geometry().x())  # 601   （以屏幕为原点的窗口横坐标）
    # 窗口离屏幕原点到x轴的距离
    print("widget.geometry().y() = %d" % widget.geometry().y())  # 238    （以屏幕为原点的窗口纵坐标，包含标题栏）
    # 窗口本身的宽度
    print("widget.geometry().width()=%d" % widget.geometry().width())  # 300    (窗口宽度)
    # 窗口本身的高度
    print("widget.geometry().height()= %d" % widget.geometry().height())  # 240    (工作区高度)

    print("第三种方式获取各个值")
    # 窗口离屏幕原点到y轴的距离
    print("widget.frameGeometry().x() = %d" % widget.frameGeometry().x())    # 600  （以屏幕为原点的窗口横坐标）
    # 窗口离屏幕原点到x轴的距离
    print("widget.frameGeometry().y() = %d" % widget.frameGeometry().y())    # 200    （以屏幕为原点的窗口纵坐标，不包含标题栏）
    # 窗口本身的宽度
    print("widget.frameGeometry().width()=%d" % widget.frameGeometry().width())    # 302   (窗口宽度)
    # 窗口本身的高度
    print("widget.frameGeometry().height()= %d" % widget.frameGeometry().height())    # 279  (窗口高度，包含标题栏)

# 将点击事件与槽绑定
btn.clicked.connect(onClick_Button)

# 移动button到窗口内的相应位置
btn.move(24,52)

# 设置窗口的尺寸
widget.resize(300,240)  # 设置工作区的尺寸

# 移动窗口到屏幕的相应位置
widget.move(600,200)

# 设置窗口的标题
widget.setWindowTitle('屏幕坐标系')

# 创建窗口
widget.show()

# 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
# 如果不添加下行代码，运行程序会闪退
sys.exit(app.exec_())
