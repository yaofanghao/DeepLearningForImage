"""
创建和使用工具栏

三种显示状态   显示图标  显示文本   显示图标和文本
图标和文本的关系：上下  左右

使用addToolBar添加
self.addToolBar()   传参  传工具栏的名字    可以创建任意多个工具栏     会从左向右排列

工具栏默认按钮：只显示图标，将文本作为悬停提示展示
"""
import sys,math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Toolbar(QMainWindow):
    def __init__(self):
        super(Toolbar, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('工具栏例子')
        # 设置尺寸大小
        self.resize(300,200)

        # 创建工具栏
        tb1 = self.addToolBar("File")

        # 往工具栏添加按钮，添加动作
        # 添加图标，添加文本
        # self  表示放在当前的窗口上
        # 工具栏默认按钮：只显示图标，将文本作为悬停提示展示
        new = QAction(QIcon('../control/images/001.jpg'),"new",self)
        # 添加new动作
        tb1.addAction(new)

        # 在工具栏添加第二个按钮
        open = QAction(QIcon('../control/images/4.jpg'),"open",self)
        # 添加open动作
        tb1.addAction(open)

        # 在工具栏添加第三个按钮
        save = QAction(QIcon('../control/images/3.ico'),"save",self)
        tb1.addAction(save)


        # 设置既显示图标又显示文本
        # 文本在图标的右侧显示
        # tb1.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        # 文本在图标的下侧显示
        tb1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        # 只显示文本
        # tb1.setToolButtonStyle(Qt.ToolButtonTextOnly)
        # 默认情况下只显示图标


        # 给tb1添加动作 用来显示按了哪一个按钮
        # 绑定信号 槽
        tb1.actionTriggered.connect(self.toolbtnpressed)

        # 让有的按钮只显示图标，有的按钮只显示文本
        # 通过创建多个工具条，一是可以将同类别的控件放在一起，二是可以控制每个工具栏相关的属性

        # 创建工具栏
        tb2 = self.addToolBar("File1")
        # 往工具栏添加动作
        new1 = QAction(QIcon('../control/images/001.png'), "new1", self)
        # 添加new1动作
        tb2.addAction(new1)
        tb2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        tb2.actionTriggered.connect(self.toolbtnpressed)

    # 槽方法
    # 显示按下的哪个按钮
    def toolbtnpressed(self,a):
        print("按下的工具栏按钮是",a.text())


# 直接运行此脚本，才会执行下面代码
if __name__ == '__main__':
    # app实例化，并传参
    app = QApplication(sys.argv)
    # 创建对象
    main = Toolbar()
    # 创建窗口
    main.show()
    # 进入主循环，调用exit方法 ，确保主循环安全退出
    sys.exit(app.exec_())
