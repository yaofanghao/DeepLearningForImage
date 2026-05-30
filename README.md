# DeepLearningForImage
* https://github.com/yaofanghao/DeepLearningForImage.git
* 2021.10起-
* 不断更新中

## 文件夹说明

* **医院项目** （项目核心）
  * 涉及敏感和关键内容不提交
  * `0-师姐项目-2022.1-2022.6/` — 前期 UNet FPNA 分割模型 + LabVIEW GUI 界面
  * `2-医学图像预处理/` — 二值化、直方图均衡化、边缘检测、超分辨率重建、Retinex 增强等预处理技术
  * `4-肠化亚型识别模型/` — 肠化亚型识别：Faster-RCNN (TF2) / YOLOv3 检测与分类，含改进模型、基线、消融实验
  * `5-综合评估模型/` — 综合评估：OLGIM 评分、胃窦胃体评估、Grad-CAM 可视化、ROC 曲线、机器学习特征分析
  * `6-软件系统设计/` — 辅助诊断软件：PyQt 桌面应用 (`PyQt_project-20231021/`) + LabVIEW 系统
  * `最新版-剪图片用这个/` — 图片裁剪、数据增强、数据集制作工具
  * `一些代码脚本/` — 日常开发实用脚本（文件读写、图像处理、格式转换等）
  
* **DeepLearningWithLabVIEW**
  * 基于 LabVIEW 实现的图像处理、深度学习项目
  * `内窥缺陷检测项目/` — 内窥镜缺陷检测：HRNet 语义分割、YOLOv5 ONNX 部署、Access 数据库集成
  * `晨光项目/` — 晨光复合材料缺陷检测分析评定软件
  * `火焰分割项目/` — 火焰分割 LabVIEW 应用（Canny/Otsu/LAB 分割）
  
* **中兴图像比赛**
  * 中兴捧月图像比赛算法：超分辨率重建（SRGAN、EDSR、WDSR）与插值算法

* **handson-ml2-master**
  * Aurelien Geron《机器学习实战》(Hands-On Machine Learning 2nd) 参考代码

* **PyQt**
  * PyQt 学习日记与代码示例（布局、信号槽、多线程、Web 等模块）

* **OpenMV**
  * OpenMV 嵌入式视觉项目：药品检测、深度学习模型（TFLite）在边缘设备上的部署

* **test_camera**
  * 摄像头采集与测试的 LabVIEW 项目（Snap/Grab/Sequence 采集模式 + ONNX 调用）

* **env**
  * 深度学习环境依赖配置文件（Tyorch/TensorFlow GPU 环境、Conda YAML 等）

## 环境依赖说明 详见env文件夹
* RTX3090 / Ubuntu20.04LTS / Python3.9
  * 依赖包参考 env/3090-tf-gpu-env.txt
  * 大致流程：
    * sudo apt-get --purge remove nvidia*
    * sudo apt autoremove 
    * ubuntu-drivers devices 
    * sudo apt install nvidia-driver-510-server 
    * conda create -n tf-gpu python==3.9 
    * conda activate tf-gpu 
    * conda install cudatoolkit=11.3 cudnn=8.2.1 
    * pip install --default-time=300 tensorflow-gpu==2.5.0 keras==2.5.0rc0
 
* RTX3090 / Ubuntu20.04LTS / Python3.8
  * 依赖包参考 env/3090-pytorch-gpu-env.txt
  * 大致流程： 
    * conda create --name pytorch-gpu python==3.8 
    * pip install torch==1.10.0+cu113 torchvision==0.11.1+cu113 torchaudio==0.10.0 -f https://download.pytorch.org/whl/torch_stable.html
  * 测试： 
    * torch.cuda.is_available()  # True 
    * torch.cuda.device_count()  # 1
    * torch.cuda.get_device_name(torch.cuda.current_device())  # NVIDIA GeForce RTX 3090'

* RTX3060 / Win11 / Python3.8.0
  * NVIDIA官网下载并配置好系统环境变量
    * CUDA == 11.3.1
    * CUDNN == 8.2.1
  * 依赖包参考 env/tf2-gpu_env.txt env/conda-gpu.yml

* 旧电脑-已不用 / Win10 / Python3.7.8
  * 依赖包参考 env/py3.7_env.txt
  * qt软件设计依赖包参考 pyqt5_env.txt
  