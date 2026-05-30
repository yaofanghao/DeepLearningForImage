from PIL import Image
import torchvision.transforms as transforms

# 加载图像
image_path = "1.jpg"
image = Image.open(image_path)

# 定义色彩变换
color_transform = transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=1, hue=1)

# 进行色彩变换
transformed_image = color_transform(image)

# 显示变换后的图像
transformed_image.show()

transformed_image.save("1_out.jpg")
