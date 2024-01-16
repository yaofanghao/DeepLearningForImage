# main函数功能：
# 实现各界面之间的跳转、交流
import sys
from PyQt5 import QtWidgets

# 调用各界面的类信息
from InitUi_InfoUi import InitUi, InfoUi
from ChanghuaUi_OLGIMUi import ChanghuaUi, OLGIMUi

# 控制器，实现各界面之间的跳转功能
class Controller:
    def __init__(self):
        # 对各窗口实例化
        self.initUi = InitUi()
        self.changhua = ChanghuaUi()
        self.olgim = OLGIMUi()
        self.info = InfoUi()

    def show_init(self):
        self.initUi.switch_changhua.connect(self.show_changhua)
        self.initUi.switch_olgim.connect(self.show_olgim)
        self.info.close()
        self.changhua.close()
        self.olgim.close()
        self.initUi.show()

    def show_info(self):
        self.initUi.close()
        # self.changhua.close()
        # self.olgim.close()
        self.info.show()

    def show_changhua(self):
        self.olgim.switch_init.connect(self.show_init)
        self.olgim.switch_info.connect(self.show_info)
        self.initUi.close()
        self.info.close()
        self.changhua.show()

    def show_olgim(self):
        self.olgim.switch_init.connect(self.show_init)
        self.olgim.switch_info.connect(self.show_info)
        self.initUi.close()
        self.info.close()
        self.olgim.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    controller = Controller()
    controller.show_init()  # 启动初始界面为InitWidget

    sys.exit(app.exec_())
