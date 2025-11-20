'''
展示整个文件夹的图片，并在图片上绘制标注框，并且保存的out目录下
'''
import os
import random
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
    print(f'label_path={label_path}')

    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            lines = f.readlines()
            for line_idx, line in enumerate(lines):
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

                # 绘制矩形框
                cv2.rectangle(image, (x, y), (x + w, y + h), color_map[class_id], 4)

                # 显示类别名称和行号
                label_text = f"{coco_class_name[class_id]}(line:{line_idx+1})"
                cv2.putText(image, label_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                           font_scale, color_map[class_id], 2)

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
img_dir = r"E:\dataSet\ymj_yolo_data\yolodata\smoke-gesture-yolo\valid\images"
label_dir = r"E:\dataSet\ymj_yolo_data\yolodata\smoke-gesture-yolo\valid\labels_person_hat_head_smoking"
output_dir = r"./out"
# coco_class_name =['people', 'unwear', 'noglove', 'unhelmet', 'insulated_ladder', 'wear', 'helmet', 'glove'] # 替换为你的类别名称
# coco_class_name = ['person','hat','head','reflectiveJacket',"hand","ladder",'glove','fall']
# coco_class_name = ["people","fall","helmet","unhelmet","vest","novest","glove","no_glove","insulated_ladder","fire"]
# coco_class_name = ['unhelmet', 'people', 'noglove', 'insulated_ladder', 'unwear']
# coco_class_name = ['box', 'ear', 'hook', 'hooked']
# coco_class_name = ['knife', 'rifle', 'gun', 'cigarette', 'alcohol']
coco_class_name = ['person','hat','head','smoking']

# 如果输出目录存在则删除
if os.path.exists(output_dir):
    import shutil
    shutil.rmtree(output_dir)
    # 重新创建输出目录
    os.makedirs(output_dir)

process_random_images(img_dir, label_dir, output_dir, num_images=9999)