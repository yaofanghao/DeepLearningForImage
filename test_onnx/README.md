# onnx部署推理测试

* 2023.7.12-
* @yaofanghao

# 在线查看onnx网络模型结构图
* https://netron.app/
* 后续模型推理，图像的输入和输出尺寸需要一一对应

# 效果测试
* onnx模型加载速度相比h5/pth可以提升5倍以上
* onnx模型推理速度相比h5/pth可以略有提升

# PyTorch 转 onnx 环境依赖
* 参考 pytorch-onnx_env.txt

# PyTorch生成的pth格式模型- 【成功】
* 详见文件夹 pytorch_pth_demo
* 1-pth2onnx.py
  * pth --> onnx
  * PyTorch对转换成onnx模型的支持较好，遇到的问题少
* 2-check_onnx.py
* 3-onnx_summary.py
* 4-onnx_pth_demo.py
  * 可以将预训练的hrnet模型的pth文件转换成onnx，且成功运行

# TensorFlow生成的h5格式模型- 【失败】
* 详见文件夹 tensorflow_h5_demo
* 1-h52onnx.py
  * h5 --> pb --> onnx
  * 可以将自己训练的hrnet模型的h5文件转换成onnx
  * 但是在实际的推理测试中，结果不准确

