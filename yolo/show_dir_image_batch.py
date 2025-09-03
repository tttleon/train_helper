'''
展示整个文件夹的图片，并在图片上绘制标注框，并且保存的out目录下
'''
import os
import random
import shutil

import cv2
import numpy as np

# 定义颜色映射，支持10个类别
color_map = {
    0: (0, 255, 0),    # 绿色
    1: (255, 0, 0),    # 蓝色
    2: (0, 0, 255),    # 红色
    3: (255, 255, 0),  # 青色
    4: (255, 0, 255),  # 品红
    5: (0, 255, 255),  # 黄色
    6: (128, 0, 128),  # 紫色
    7: (128, 128, 0),  # 橄榄色
    8: (0, 128, 128),  # 青绿色
    9: (128, 128, 128)   # 灰色
}




def draw_and_save_image(img_path, label_path, output_path):
    """
    !!! 注意，路径里面不能存在中文字符，否则会报错
    !!! 注意，路径里面不能存在中文字符，否则会报错
    !!! 注意，路径里面不能存在中文字符，否则会报错
    """
    image = cv2.imread(img_path)
    height, width, _ = image.shape

    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split()
                if len(parts) < 5:
                    continue  # skip malformed lines

                # class_id = int(parts[0])
                class_id = int(float(parts[0]))
                x_center, y_center, w, h = map(float, parts[1:])
                x = int((x_center - w / 2) * width)
                y = int((y_center - h / 2) * height)
                w = int(w * width)
                h = int(h * height)
                # 动态计算字体大小
                font_scale = max(0.5, min(2, w / 100))  # 根据宽度调整字体大小
                cv2.rectangle(image, (x, y), (x + w, y + h), color_map[class_id], 4)
                cv2.putText(image, f"{coco_class_name[class_id]}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color_map[class_id], 2)

    # 保存结果图像
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, image)

def process_random_images(img_dir, label_dir, output_dir, num_images=5):
    all_images = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    selected_images = random.sample(all_images, min(num_images, len(all_images)))

    for img_file in selected_images:
        img_path = os.path.join(img_dir, img_file)
        label_file = os.path.splitext(img_file)[0] + '.txt'
        label_path = os.path.join(label_dir, label_file)
        output_path = os.path.join(output_dir, img_file)

        print(f"Processing {img_file}...")
        draw_and_save_image(img_path, label_path, output_path)

# ==== 配置路径和数量 ====
# 多个输入目录，包含 images 和 labels 子目录
base_dirs = [
    r'E:\dataSet\ymj_yolo_data\yolodata\person-hat-head\valid',
    r'E:\dataSet\ymj_yolo_data\yolodata\helmet-reflectiveJacket\valid',
    r'E:\dataSet\ymj_yolo_data\yolodata\Glove\valid',
    r'E:\dataSet\ymj_yolo_data\yolodata\Glove\valid-arg',
    r'E:\dataSet\ymj_yolo_data\yolodata\ladders-2\valid',
    r'E:\dataSet\ymj_yolo_data\yolodata\ladders-2\valid-arg',
    r'E:\dataSet\ymj_yolo_data\yolodata\ladder-dianxin\valid',
    r'E:\dataSet\ymj_yolo_data\yolodata\ladder-dianxin\valid-arg',
    r'E:\dataSet\ymj_yolo_data\yolodata\fall-haitu\valid',
]

output_root = r"./out"

coco_class_name = ["people","fall","helmet","unhelmet","vest","novest","glove","no_glove","insulated_ladder","fire"]

# 如果输出目录存在则删除
if os.path.exists(output_root):
    shutil.rmtree(output_root)
os.makedirs(output_root)

# 遍历每个目录
for base_dir in base_dirs:
    img_dir = os.path.join(base_dir, "images")
    label_dir = os.path.join(base_dir, "labels")

    # 取父目录名和当前目录名拼接
    parent_name = os.path.basename(os.path.dirname(base_dir))
    cur_name = os.path.basename(base_dir)
    sub_name = f"{parent_name}-{cur_name}"

    output_dir = os.path.join(output_root, sub_name)
    os.makedirs(output_dir, exist_ok=True)

    # 调用处理函数
    process_random_images(img_dir, label_dir, output_dir, num_images=10)
