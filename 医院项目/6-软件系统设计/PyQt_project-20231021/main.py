"""
main函数功能：
  实现各界面之间的跳转、交流，并在后台预加载模型
"""
import sys
import logging

from PyQt5 import QtCore, QtWidgets

from ui_controller import InitUi, InfoUi, ChanghuaUi, OLGIMUi
from model_loader import ModelLoadWorker, ModelManager

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG,
)
logger = logging.getLogger(__name__)


class Controller(QtCore.QObject):
    """控制器：管理界面跳转 + 后台模型预加载"""
    _models_ready = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        # 实例化所有窗口（仅一次）
        self.initUi = InitUi()
        self.changhua = ChanghuaUi()
        self.olgim = OLGIMUi()
        self.info = InfoUi()

        # 一次性连接信号（避免重复连接导致 slot 多次触发）
        self._connect_signals()

        # 后台线程预加载模型
        self._start_model_loading()

    def _connect_signals(self):
        """一次性连接所有窗口的信号"""
        # InitUi → 其他页面
        self.initUi.switch_changhua.connect(self.show_changhua)
        self.initUi.switch_olgim.connect(self.show_olgim)

        # ChanghuaUi → 初始 / 报告页面
        self.changhua.switch_init.connect(self.show_init)
        self.changhua.switch_info.connect(self.show_info)

        # OLGIMUi → 初始 / 报告 / GradCAM 页面
        self.olgim.switch_init.connect(self.show_init)
        self.olgim.switch_info.connect(self.show_info)

    def _start_model_loading(self):
        """在后台线程中预加载模型"""
        self._model_thread = QtCore.QThread(self)
        self._model_worker = ModelLoadWorker()
        self._model_worker.moveToThread(self._model_thread)

        self._model_thread.started.connect(self._model_worker.run)
        self._model_worker.finished.connect(self._on_models_loaded)
        self._model_worker.error.connect(self._on_model_error)
        self._model_worker.finished.connect(self._model_thread.quit)
        self._model_worker.finished.connect(self._model_worker.deleteLater)
        self._model_thread.finished.connect(self._model_thread.deleteLater)

        self._model_thread.start()

    def _on_models_loaded(self, models):
        """模型加载完成后保存到 ModelManager"""
        ModelManager().set_models(models)
        logger.info("所有模型加载完成")
        self._models_ready.emit()

    def _on_model_error(self, error_msg):
        logger.error("模型加载失败: %s", error_msg)

    # ----- 界面切换 -----
    def show_init(self):
        self.info.close()
        self.changhua.close()
        self.olgim.close()
        self.initUi.show()

    def show_info(self):
        self.initUi.close()
        self.info.show()

    def show_changhua(self):
        self.initUi.close()
        self.info.close()
        self.olgim.close()
        self.changhua.show()

    def show_olgim(self):
        self.initUi.close()
        self.info.close()
        self.olgim.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    controller = Controller()
    controller.show_init()

    sys.exit(app.exec_())
