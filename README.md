# DeepLearningForImage
* https://github.com/yaofanghao/DeepLearningForImage.git
* 2021.10起-
* 不断更新中

## 文件夹说明
* 医院项目
  * 涉及敏感和关键内容不提交
 
* DeepLearningWithLabVIEW
  * 基于LabVIEW实现的图像处理、深度学习项目

* handson-ml2-master
  * Aurelien Geron《机器学习实战》参考代码

* PyQt
  * PyQt的学习日记、代码

* test_onnx
  * onnx模型推理部署示例
  
* 其他常用脚本、示例、参考书

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
  