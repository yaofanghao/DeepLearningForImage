"""
模型加载器：在后台线程预加载 FRCNN 模型，避免界面卡顿
"""
import logging

from PyQt5 import QtCore

from config import (
    CONFIDENCE_THRESHOLD, NMS_IOU,
    MODEL_PATH_CHANGHUA, CLASSES_PATH_CHANGHUA,
    MODEL_PATH_OLGIM, CLASSES_PATH_OLGIM,
)
from nets.frcnn_class import FRCNN

logger = logging.getLogger(__name__)


class ModelLoadWorker(QtCore.QObject):
    """后台加载模型的 Worker（在 QThread 中运行）"""
    finished = QtCore.pyqtSignal(dict)
    progress = QtCore.pyqtSignal(str)
    error = QtCore.pyqtSignal(str)

    def run(self):
        """加载所有模型"""
        models = {}
        try:
            self.progress.emit("正在加载肠化模型...")
            models['changhua'] = FRCNN(
                model_path=MODEL_PATH_CHANGHUA,
                classes_path=CLASSES_PATH_CHANGHUA,
                confidence=CONFIDENCE_THRESHOLD,
                nms_iou=NMS_IOU,
            )
            self.progress.emit("肠化模型加载完成")

            self.progress.emit("正在加载 OLGIM 模型...")
            models['olgim'] = FRCNN(
                model_path=MODEL_PATH_OLGIM,
                classes_path=CLASSES_PATH_OLGIM,
                confidence=CONFIDENCE_THRESHOLD,
                nms_iou=NMS_IOU,
            )
            self.progress.emit("OLGIM 模型加载完成")

            self.finished.emit(models)
        except Exception as e:
            logger.exception("模型加载失败")
            self.error.emit(str(e))


class ModelManager:
    """模型管理器（单例），提供全局访问点"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._models = {}
            cls._instance._loaded = False
        return cls._instance

    def get_model(self, name):
        return self._models.get(name)

    @property
    def is_loaded(self):
        return self._loaded

    @is_loaded.setter
    def is_loaded(self, value):
        self._loaded = value

    def get_models(self):
        return self._models

    def set_models(self, models):
        self._models = models
        self._loaded = True
