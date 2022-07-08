# coding:utf-8
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

import paddlex as pdx
predictor = pdx.deploy.Predictor(model_dir='inference_model/inference_model',
                                    use_gpu=True)
result = predictor.predict(img_file='imgtest/100.jpg',
                           warmup_iters=100,
                           repeats=200)
