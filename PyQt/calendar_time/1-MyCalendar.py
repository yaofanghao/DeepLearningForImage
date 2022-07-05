"""
日历控件
QCalendarWidget
"""
# 允许用户选择日期
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyCalendar(QWidget):
    def __init__(self):
        super(MyCalendar, self).__init__()
        self.initUI()

    # 编写初始化方法，规范代码，初始化写在一个方法里
    def initUI(self):
        # 创建日历控件，全局的，在单击事件里面调用
        self.cal = QCalendarWidget(self)
        # 创建label控件，用于显示当前选择的日期
        # 这个label用绝对布局
        self.label = QLabel(self)
        # 显示当前日期
        date = self.cal.selectedDate()
        self.label.setText(date.toString('yyyy-MM-dd dddd'))
        # 移动label到相应的位置
        self.label.move(20,300)
        # 设置允许显示最小日期
        self.cal.setMinimumDate(QDate(1988,1,1))
        # 设置允许显示的最大日期
        self.cal.setMaximumDate(QDate(2088,1,1))


        # 绑定信号 槽
        self.cal.clicked.connect(self.showDate)

        # 以网格形式显示
        self.cal.setGridVisible(True)

        # 移动日历的位置  移动到左上角
        self.cal.move(20,20)

        # 设置窗口大小
        self.resize(400,400)

        # 设置标题
        self.setWindowTitle('日历演示')
    # 添加单击事件
    # 槽
    def showDate(self,date):
        # 显示当前选择的日期
        # 方式一  直接在事件里面获取
        # self.label.setText((date.toString('yyyy-MM-dd dddd')))
        # 方式二   直接通过日历，里面有个selcetedDate的方法获取
        self.label.setText((self.cal.selectedDate().toString("yyyy-MM-dd dddd")))


# 防止其他脚本调用，只有单独运行，才会调用下面代码
if __name__ == '__main__':
    # app实例化，传参
    app = QApplication(sys.argv)
    # 创建对象
    main = MyCalendar()
    # 创建窗口
    main.show()
    # 进入主循环，调用exit方法，确保主循环安全退出
    sys.exit(app.exec_())
