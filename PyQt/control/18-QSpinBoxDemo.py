"""
计数器控件(QSpinBox)
用来控制一个数字的增加或减少
"""

# 显示数字，获取数字，查看数字变化
import sys
# QtCore是Qt的精髓（包括五大模块：元对象系统，属性系统，对象模型，对象树，信号槽）
from PyQt5.QtCore import *
# QtGui 显示应用程序图标，工具提示和各种鼠标光标。
from PyQt5.QtGui import *
# Qt Widgets模块提供了一组UI元素来创建经典的桌面风格的用户界面。
from PyQt5.QtWidgets import *


class QSpinBoxDemo(QWidget):
    def __init__(self):
        super(QSpinBoxDemo, self).__init__()
        self.initUI()


    # 编写初始化方法
    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle('QSpinBox演示')
        # 设置窗口尺寸
        self.resize(300,100)

        # 创建垂直布局
        layout = QVBoxLayout()

        # 创建label控件
        self.label = QLabel('当前值')
        # 设置label控件的文字居中
        self.label.setAlignment(Qt.AlignCenter)


        # 创建QSpinBox控件
        self.sb = QSpinBox()
        #给控件设置默认值，从18开始变
        self.sb .setValue(18)
        #给控件设置范围，最小为19，最大为42
        self.sb.setRange(19,42)
        # 添加步长，让每次增3
        self.sb.setSingleStep(3)
        # 把控件添加到垂直布局里
        layout.addWidget(self.label)
        layout.addWidget(self.sb)

        # 信号槽绑定
        # 当value值发生变化时的方法
        self.sb.valueChanged.connect(self.valueChange)

        # 应用于垂直布局
        self.setLayout(layout)

    # 槽方法
    def valueChange(self):
        # 获得的字段
        self.label.setText('当前值：' + str(self.sb.value()))


# 防止别的脚本调用，只有自己单独运行时，才会调用下面代码
if __name__ == '__main__':
    # 创建app实例，并传入参数
    app= QApplication(sys.argv)
    # 创建对象
    main = QSpinBoxDemo()
    # 创建窗口
    main.show()
    # 进入程序的主循环，并通过exit函数，确保主循环安全结束(该释放资源的释放资源)
    sys.exit(app.exec_())

