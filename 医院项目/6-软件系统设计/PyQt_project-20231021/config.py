"""
配置文件：集中管理路径、阈值等常量
"""
import os


# ---------- 路径配置 ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 模型路径
MODEL_PATH_CHANGHUA = os.path.join(BASE_DIR, 'nets', 'logs_Changhua.h5')
CLASSES_PATH_CHANGHUA = os.path.join(BASE_DIR, 'nets', 'voc_classes_Changhua.txt')
MODEL_PATH_OLGIM = os.path.join(BASE_DIR, 'nets', 'logs_OLGIM.h5')
CLASSES_PATH_OLGIM = os.path.join(BASE_DIR, 'nets', 'voc_classes_OLGIM.txt')

# 输出路径
OUTPUT_DIR_CHANGHUA = os.path.join(BASE_DIR, 'img_out_Changhua')
OUTPUT_DIR_OLGIM = os.path.join(BASE_DIR, 'img_out_OLGIM')
OUTPUT_DIR_INFO_REPORT = os.path.join(BASE_DIR, 'img_out_report')

# ---------- 模型参数 ----------
CONFIDENCE_THRESHOLD = 0.5
NMS_IOU = 0.1
ANCHORS_SIZE = [128, 256, 512]

# ---------- 报告字体路径 ----------
FONT_PATH = os.path.join(BASE_DIR, 'pdf', 'yangziti.ttf')
