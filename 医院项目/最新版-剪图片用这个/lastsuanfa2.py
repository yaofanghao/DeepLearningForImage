# coding:utf-8
"""
图像自动裁剪工具
通过 Sobel 边缘检测 + 形态学梯度 + 轮廓提取 找到图像主体区域并裁剪。
支持批量处理文件夹下所有图片。

使用方法：修改本文件末尾的 DATADIR 和 save_dir 路径后运行。
"""
import os
import cv2
import numpy as np

# ==================== 可调参数 ====================
SOBEL_KERNEL_SIZE = 5
GAUSSIAN_BLUR_SIZE = (3, 3)
CANNY_THRESHOLD_LOW = 50
CANNY_THRESHOLD_HIGH = 150
BINARY_THRESHOLD = 210
MORPH_KERNEL_SIZE = (5, 5)
ADAPTIVE_BLOCK_SIZE = 3
ADAPTIVE_C = 10
# ==================================================


def _save_intermediate(prefix, filename, image):
    """调试时保存中间结果图（取消注释即可启用）"""
    # cv2.imwrite(f"{prefix}_{filename}", image)
    pass


def find_crop_bounds(image_path):
    """对单张图片进行边缘检测，返回裁剪边界 (Ymin, Ymax, Xmin, Xmax)。"""
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"无法读取图片: {image_path}")
    h, w = img.shape[:2]

    # ---------- 1. Sobel 水平边缘检测 ----------
    sobel_horizontal = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=SOBEL_KERNEL_SIZE)
    sobel_img = cv2.convertScaleAbs(sobel_horizontal)
    _save_intermediate("debug", "sobel.jpg", sobel_img)

    # ---------- 2. Canny 边缘检测 ----------
    blurred = cv2.GaussianBlur(sobel_img, GAUSSIAN_BLUR_SIZE, 0)
    canny = cv2.Canny(blurred, CANNY_THRESHOLD_LOW, CANNY_THRESHOLD_HIGH)
    _save_intermediate("debug", "canny.jpg", canny)

    # ---------- 3. 形态学梯度 ----------
    _, thr_img = cv2.threshold(sobel_img, BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, MORPH_KERNEL_SIZE)
    gradient = cv2.morphologyEx(thr_img, cv2.MORPH_GRADIENT, kernel)
    _save_intermediate("debug", "gradient.jpg", gradient)

    # ---------- 4. 自适应阈值 + 轮廓提取 ----------
    gray = cv2.cvtColor(gradient, cv2.COLOR_BGR2GRAY) if gradient.ndim == 3 else gradient
    dst = cv2.adaptiveThreshold(
        gray, 210, cv2.BORDER_REPLICATE,
        cv2.THRESH_BINARY_INV, ADAPTIVE_BLOCK_SIZE, ADAPTIVE_C,
    )
    contours, _ = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return 0, h, 0, w

    # ---------- 5. 计算最大外接矩形 ----------
    max_area = -1
    best_box = (0, 0, 0, 0)
    for c in contours:
        x, y, bw, bh = cv2.boundingRect(c)
        area = bw * bh
        if area > max_area:
            max_area = area
            best_box = (y, y + bh, x, x + bw)

    return best_box


def batch_crop_images(input_dir, output_dir, log_file="crop_log.txt"):
    """批量裁剪 input_dir 下的所有图片，结果保存到 output_dir。"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_names = [f for f in os.listdir(input_dir)
                   if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
    image_names.sort()  # 按文件名自然排序

    results = []
    for idx, fname in enumerate(image_names):
        src_path = os.path.join(input_dir, fname)
        print(f"[{idx+1}/{len(image_names)}] 处理: {fname}")

        try:
            ymin, ymax, xmin, xmax = find_crop_bounds(src_path)
            img = cv2.imread(src_path)
            cropped = img[ymin:ymax, xmin:xmax]

            out_name = f"{idx}.jpg"
            out_path = os.path.join(output_dir, out_name)
            cv2.imwrite(out_path, cropped)

            results.append((fname, ymin, ymax, xmin, xmax))
        except Exception as e:
            print(f"  [!] 跳过 {fname}: {e}")

    # 将裁剪坐标写入日志文件
    with open(log_file, 'w', encoding='utf-8') as f:
        for fname, ymin, ymax, xmin, xmax in results:
            f.write(f"{fname} {ymin} {ymax} {xmin} {xmax}\n")

    print(f"完成！共处理 {len(results)} 张图片，日志已保存至 {log_file}")


if __name__ == '__main__':
    # ==================== 修改区域 ====================
    DATADIR = "C:\\Users\\admin\\Desktop\\dataset\\jpg1"   # 原图片路径（请修改）
    save_dir = "C:\\Users\\admin\\Desktop\\dataset\\jpg2"  # 裁剪后保存路径（请修改）
    # ==================================================
    batch_crop_images(DATADIR, save_dir)
