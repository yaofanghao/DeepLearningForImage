import os
import tensorflow as tf
from PIL import Image
from tqdm import tqdm
from hrnet import HRnet_Segmentation
from utils.utils_metrics import compute_mIoU, show_results

gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

# envpath = '/home/ubuntu/anaconda3/envs/tf-gpu/lib/python3.9/site-packages/cv2/qt/plugins/platforms'
# os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = envpath


'''
进行指标评估需要注意以下几点：
1、该文件生成的图为灰度图，因为值比较小，按照PNG形式的图看是没有显示效果的，所以看到近似全黑的图是正常的。
2、该文件计算的是验证集的miou，当前该库将测试集当作验证集使用，不单独划分测试集
'''
if __name__ == "__main__":
    num_classes     = 11    #   分类个数+1、如2+1
    name_classes    = ["background","duoyuwu","aokeng","qipi","cashang","gubo","xiuban","baiban","yanghuawu",
                       "huashang","hanjiequexian"]    #   区分的种类，和json_to_dataset里面的一样
    VOCdevkit_path  = 'VOCdevkit'

    image_ids       = open(os.path.join(VOCdevkit_path, "VOC2007/ImageSets/Main/val.txt"),'r').read().splitlines()
    gt_dir          = os.path.join(VOCdevkit_path, "VOC2007/SegmentationClass/")
    miou_out_path   = "miou_out"
    pred_dir        = os.path.join(miou_out_path, 'detection-results')
    dir_save_path   = "img_out/"
    if not os.path.exists(pred_dir):
        os.makedirs(pred_dir)
    if not os.path.exists(miou_out_path):
        os.makedirs(miou_out_path)
    if not os.path.exists(dir_save_path):
        os.makedirs(dir_save_path)

    print("Load model.")
    hrnet = HRnet_Segmentation()
    print("Load model done.")

    print("Get predict result.")
    for image_id in tqdm(image_ids):
        image_path  = os.path.join(VOCdevkit_path, "VOC2007/JPEGImages/"+image_id+".jpg")
        image       = Image.open(image_path)
        image       = hrnet.get_miou_png(image)
        image.save(os.path.join(pred_dir, image_id + ".png"))

        # 获取预测图片
        image       = Image.open(image_path)
        r_image = hrnet.detect_image(image,name_classes=name_classes)
        r_image.save(os.path.join(dir_save_path, image_id + ".png"))
    print("Get predict result done.")

    print("Get miou.")
    hist, IoUs, PA_Recall, Precision = compute_mIoU(gt_dir, pred_dir, image_ids, num_classes, name_classes)  # 执行计算mIoU的函数
    print("Get miou done.")
    show_results(miou_out_path, hist, IoUs, PA_Recall, Precision, name_classes)
    print("show results done")

