import os
import sys
from yolo import YOLO

simplify = True
# onnx_save_path = "model_data/models.onnx"
onnx_save_path =  sys.argv[1]


(filepath, filename) = os.path.split(onnx_save_path)
if not os.path.exists(filepath):
    os.makedirs(filepath)

yolo = YOLO(model_path=sys.argv[2],phi=sys.argv[3],cuda=sys.argv[4].lower() == 'true')
yolo.convert_to_onnx(simplify, onnx_save_path)