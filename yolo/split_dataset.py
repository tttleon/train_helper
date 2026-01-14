import os
import shutil
import random

# 基础路径
base_dir = r"E:\dataSet\ymj_yolo_data\yolodata\ARDS-knif-pisto-rifle-stick"
# 是否划分测试集
is_split_test = False

# 总图片数据和标签的路径
images_dir = os.path.join(base_dir, "train", "images")
labels_dir = os.path.join(base_dir, "train", "labels")

# 验证集目标路径
valid_images_dir = os.path.join(base_dir, "valid", "images")
valid_labels_dir = os.path.join(base_dir, "valid", "labels")


# 测试集目标路径
test_images_dir = os.path.join(base_dir, "test", "images")
test_labels_dir = os.path.join(base_dir, "test", "labels")



# 创建目标文件夹
for d in [valid_images_dir, valid_labels_dir]:
    os.makedirs(d, exist_ok=True)

if (is_split_test):
    for d in [test_images_dir, test_labels_dir]:
        os.makedirs(d, exist_ok=True)


# 获取所有图像文件（假设为 .jpg，可以改为你实际使用的格式）
image_files = [f for f in os.listdir(images_dir) if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".JPG") or f.endswith(".PNG")]

# 打乱顺序
random.shuffle(image_files)

total = len(image_files)
val_count = int(total * 0.15)
test_count = int(total * 0.10)

val_files = image_files[:val_count]
test_files = image_files[val_count:val_count + test_count]


def move_files(file_list, target_img_dir, target_lbl_dir):
    for img_file in file_list:
        label_file = os.path.splitext(img_file)[0] + ".txt"
        src_img = os.path.join(images_dir, img_file)
        src_lbl = os.path.join(labels_dir, label_file)

        dst_img = os.path.join(target_img_dir, img_file)
        dst_lbl = os.path.join(target_lbl_dir, label_file)

        if os.path.exists(src_img) and os.path.exists(src_lbl):
            shutil.move(src_img, dst_img)
            shutil.move(src_lbl, dst_lbl)


# 移动验证集和测试集
move_files(val_files, valid_images_dir, valid_labels_dir)

if (is_split_test):
    move_files(test_files, test_images_dir, test_labels_dir)

print(f"验证集划分完成：{len(val_files)}张图片")
if (is_split_test):
    print(f"测试集划分完成：{len(test_files)}张图片")

if(is_split_test):
    print(f"训练集剩余：{total - val_count - test_count}张图片")
else:
    print(f"训练集剩余：{total - val_count}张图片")
