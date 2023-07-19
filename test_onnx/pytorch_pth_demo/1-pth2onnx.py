"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/7/13 15:50
    @Filename: 1-pth2onnx.py
    @Software: PyCharm     
"""


import torch
# import torchvision

from nets.hrnet import HRnet

if __name__ == "__main__":
    input_shape     = [480, 480]
    num_classes     = 9
    backbone        = 'hrnetv2_w18'
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # 加载训练好的PyTorch模型
    # model = torchvision.models.resnet18()
    model = HRnet(num_classes=num_classes, backbone=backbone, pretrained=False).to(device)

    model.load_state_dict(torch.load('best_epoch_weights.pth', map_location='cpu'))
    model.eval()

    # 创建用于输入的示例张量
    dummy_input = torch.randn(1, 3, 480, 480)  # 示例输入大小为 (batch_size, channels, height, width)

    # 导出为ONNX模型
    input_names = ["images"]
    output_names = ["output"]
    onnx_file_path = "hrnet_from_pytorch.onnx"
    torch.onnx.export(model, dummy_input, onnx_file_path,
                      input_names=input_names, output_names=output_names, opset_version=11)

    print("ONNX 模型已成功导出：", onnx_file_path)
