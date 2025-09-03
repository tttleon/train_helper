'''
yolo根据指定类别过滤图片和标签文件

原始标签：names: ['SafetyShoe', 'faceMask', 'goggle', 'helmet', 'no_faceMask', 'no_gloves', 'no_helmet', 'no_vest', 'object', 'person', 'vest']

指定需要的标签 ['no_gloves']

原始目录 ：
    E:\dataSet\ymj_yolo_data\yolodata\Safety_DS.v1i.yolov5pytorch\train\images
    E:\dataSet\ymj_yolo_data\yolodata\Safety_DS.v1i.yolov5pytorch\train\labels

输出目录：
    E:\dataSet\ymj_yolo_data\yolodata\Safety_DS.v1i.yolov5pytorch\train-filter\images
    E:\dataSet\ymj_yolo_data\yolodata\Safety_DS.v1i.yolov5pytorch\train-filter\labels

遍历原始目录下的所有图片和标签文件，检查标签文件中是否包含指定类别，如果包含则复制到输出目录。
'''


import os
import shutil

# 类别映射
names = ['SafetyShoe', 'faceMask', 'goggle', 'helmet', 'no_faceMask', 'no_gloves',
         'no_helmet', 'no_vest', 'object', 'person', 'vest']

# 指定需要的类别
target_classes = ['no_gloves']
target_class_ids = [names.index(cls) for cls in target_classes]

# 原始目录
images_dir = r'E:\dataSet\ymj_yolo_data\yolodata\Safety_DS.v1i.yolov5pytorch\valid\images'
labels_dir = r'E:\dataSet\ymj_yolo_data\yolodata\Safety_DS.v1i.yolov5pytorch\valid\labels'

# 输出目录
out_images_dir = r'E:\dataSet\ymj_yolo_data\yolodata\Safety_DS.v1i.yolov5pytorch\valid-filter\images'
out_labels_dir = r'E:\dataSet\ymj_yolo_data\yolodata\Safety_DS.v1i.yolov5pytorch\valid-filter\labels'

# 创建输出目录（如果不存在）
os.makedirs(out_images_dir, exist_ok=True)
os.makedirs(out_labels_dir, exist_ok=True)

# 遍历标签文件
for label_file in os.listdir(labels_dir):
    if not label_file.endswith('.txt'):
        continue

    label_path = os.path.join(labels_dir, label_file)

    with open(label_path, 'r') as f:
        lines = f.readlines()

    # 检查是否包含指定类别
    has_target_class = any(int(line.split()[0]) in target_class_ids for line in lines)

    if has_target_class:
        # 拷贝标签文件
        shutil.copy(label_path, os.path.join(out_labels_dir, label_file))

        # 拷贝对应的图片文件（.jpg/.png）
        base_name = os.path.splitext(label_file)[0]
        for ext in ['.jpg', '.png', '.jpeg', '.JPG', '.PNG', '.JPEG']:
            img_path = os.path.join(images_dir, base_name + ext)
            if os.path.exists(img_path):
                shutil.copy(img_path, os.path.join(out_images_dir, os.path.basename(img_path)))
                break
