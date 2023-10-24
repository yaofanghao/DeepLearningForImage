"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/10/23 16:01
    @Filename: 中间层特征可视化.py
    @Software: PyCharm     
"""

"""
import torch
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from torchvision import transforms
from nets.frcnn import FasterRCNN

data_transform = transforms.Compose(
    [transforms.Resize((600, 600)),
     transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

model = FasterRCNN(num_classes=20)
model_weight_path = "model_data/voc_weights_resnet.pth"
pre_weights = torch.load(model_weight_path, map_location=torch.device('cpu'))

# 遍历state_dict并打印模型中的层数
for name, param in pre_weights.items():
    print(f'{name}: {param.shape}')

print("success load model")

pre_weights.pop('extractor.0.weight')
pre_weights.pop('rpn.conv1.weight')
pre_weights.pop('head.cls_loc.weight')
pre_weights.pop('head.score.weight')

model.load_state_dict(pre_weights, strict=False)

print(model)

img = Image.open("street.jpg")
# [N, C, H, W]
img = data_transform(img)
img = torch.unsqueeze(img, dim=0)

# forward
out_put = model(img)
for feature_map in out_put:
    # [N, C, H, W] -> [C, H, W]
    # im = np.squeeze(feature_map.detach().numpy())
    im = feature_map.detach().numpy()

    # [C, H, W] -> [H, W, C]print(model)
    im = np.transpose(im, [1, 2, 0])


    # show top 12 feature maps
    plt.figure()
    for i in range(12):
        ax = plt.subplot(3, 4, i+1)#行，列，索引
        # [H, W, C]
        plt.imshow(im[:, i])#cmap默认为蓝绿图
    plt.show()
"""

