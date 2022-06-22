# coding:utf-8
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

import paddlex as pdx
predictor = pdx.deploy.Predictor(model_dir='yolov3_darknet53_coco/inference_model',
                                    use_gpu=True)
result = predictor.predict(img_file='img/7.jpg',
                           warmup_iters=100,
                           repeats=200)
