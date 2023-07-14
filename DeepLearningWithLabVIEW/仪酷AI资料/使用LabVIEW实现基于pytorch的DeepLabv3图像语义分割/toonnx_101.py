import os
import torch
import torch.onnx
from torch.autograd import Variable
from torchvision import models
import re

dirname, filename = os.path.split(os.path.abspath(__file__))
print(dirname)

def get_pytorch_onnx_model(original_model):
    # define the directory for further converted model save
    onnx_model_path = dirname
    # define the name of further converted model
    onnx_model_name = "deeplabv3_resnet101.onnx"

    # create directory for further converted model
    os.makedirs(onnx_model_path, exist_ok=True)

    # get full path to the converted model
    full_model_path = os.path.join(onnx_model_path, onnx_model_name)

    # generate model input
    generated_input = Variable(
        torch.randn(1, 3, 448, 448)
    )

    # model export into ONNX format
    torch.onnx.export(
        original_model,
        generated_input,
        full_model_path,
        verbose=True,
        input_names=["input"],
        output_names=["output",'aux'],
        opset_version=11
    )

    return full_model_path


def main():
    # initialize PyTorch ResNet-101 model
    original_model = models.segmentation.deeplabv3_resnet101(pretrained=True)

    # get the path to the converted into ONNX PyTorch model
    full_model_path = get_pytorch_onnx_model(original_model)
    print("PyTorch ResNet-101 model was successfully converted: ", full_model_path)


if __name__ == "__main__":
    main()
