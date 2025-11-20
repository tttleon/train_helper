import os
from PIL import Image
import matplotlib.pyplot as plt

# 图片目录
img_dir = r"E:\dataSet\ocr\mcc_icon\train_data_crop_oriented\rec\train"

widths = []
heights = []

# 遍历文件
for root, _, files in os.walk(img_dir):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')):
            img_path = os.path.join(root, file)
            try:
                with Image.open(img_path) as img:
                    w, h = img.size
                    widths.append(w)
                    heights.append(h)
            except Exception as e:
                print(f"跳过文件 {img_path}, 错误: {e}")

# 绘制宽度分布
plt.figure(figsize=(10, 5))
plt.hist(widths, bins=50, edgecolor='black')
plt.title("Width Distribution")
plt.xlabel("Width (pixels)")
plt.ylabel("Count")
plt.show()

# 绘制高度分布
plt.figure(figsize=(10, 5))
plt.hist(heights, bins=50, edgecolor='black')
plt.title("Height Distribution")
plt.xlabel("Height (pixels)")
plt.ylabel("Count")
plt.show()
