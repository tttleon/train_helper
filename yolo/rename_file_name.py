import os
import random
import string
import shutil

# 原始路径
images_dir = r"E:\dataSet\ymj_yolo_data\yolodata\Glove\train\images"
labels_dir = r"E:\dataSet\ymj_yolo_data\yolodata\Glove\train\labels"

# 输出路径
output_images_dir = r"E:\dataSet\ymj_yolo_data\yolodata\Glove\train_rename\images"
output_labels_dir = r"E:\dataSet\ymj_yolo_data\yolodata\Glove\train_rename\labels"

# 创建输出目录
os.makedirs(output_images_dir, exist_ok=True)
os.makedirs(output_labels_dir, exist_ok=True)

# 获取所有图片文件
image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'))]

# 随机文件名生成函数
def random_filename(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# 存储已用随机名，避免重复
used_names = set()

for img_file in image_files:
    base_name, ext = os.path.splitext(img_file)

    # 生成唯一的新文件名
    while True:
        new_name = random_filename()
        if new_name not in used_names:
            used_names.add(new_name)
            break

    # 定义原路径
    old_img_path = os.path.join(images_dir, img_file)
    old_label_path = os.path.join(labels_dir, base_name + ".txt")

    # 定义新路径
    new_img_path = os.path.join(output_images_dir, new_name + ext)
    new_label_path = os.path.join(output_labels_dir, new_name + ".txt")

    # 复制图片
    shutil.copy2(old_img_path, new_img_path)

    # 复制标签（如果存在）
    if os.path.exists(old_label_path):
        shutil.copy2(old_label_path, new_label_path)
    else:
        print(f"⚠️ 标签文件不存在：{base_name}.txt")

    print(f"✅ 已处理：{img_file} → {new_name + ext}")
