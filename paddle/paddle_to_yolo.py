import json
import os
import shutil
from pathlib import Path


def convert_paddle_to_yolo(paddle_label_path, paddle_img_dir, output_img_dir, output_label_dir):
    """
    将Paddle格式的JSON标注转换为YOLO格式

    Args:
        paddle_label_path: Paddle标注JSON文件路径
        paddle_img_dir: 原始图片目录
        output_img_dir: 输出图片目录
        output_label_dir: 输出标签目录
    """

    # 创建输出目录
    os.makedirs(output_img_dir, exist_ok=True)
    os.makedirs(output_label_dir, exist_ok=True)

    # 读取JSON文件
    with open(paddle_label_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 创建类别映射（这里只有一个类别cigarette）
    categories = {cat['id']: cat['name'] for cat in data['categories']}
    print(f"找到类别: {categories}")

    # 创建图像ID到文件名的映射
    image_id_to_file = {img['id']: img['file_name'] for img in data['images']}
    image_id_to_size = {img['id']: (img['width'], img['height']) for img in data['images']}

    # 按图像分组标注
    annotations_by_image = {}
    for ann in data['annotations']:
        image_id = ann['image_id']
        if image_id not in annotations_by_image:
            annotations_by_image[image_id] = []
        annotations_by_image[image_id].append(ann)

    # 处理每个图像
    processed_count = 0
    for image_id, annotations in annotations_by_image.items():
        if image_id not in image_id_to_file:
            print(f"警告: 图像ID {image_id} 没有对应的文件信息")
            continue

        # 获取图像信息
        image_file = image_id_to_file[image_id]
        image_width, image_height = image_id_to_size[image_id]

        # 源图像路径
        src_image_path = os.path.join(paddle_img_dir, image_file)

        if not os.path.exists(src_image_path):
            print(f"警告: 图像文件不存在: {src_image_path}")
            continue

        # 目标图像路径（保持原文件名）
        dst_image_path = os.path.join(output_img_dir, image_file)

        # 复制图像文件
        shutil.copy2(src_image_path, dst_image_path)

        # 创建对应的标签文件
        label_file = os.path.splitext(image_file)[0] + '.txt'
        label_path = os.path.join(output_label_dir, label_file)

        # 转换标注为YOLO格式
        with open(label_path, 'w', encoding='utf-8') as f:
            for ann in annotations:
                # 获取边界框信息
                bbox = ann['bbox']  # [x, y, width, height]
                category_id = ann['category_id']

                # 转换为YOLO格式: [class_id, x_center, y_center, width, height] (归一化坐标)
                x_center = (bbox[0] + bbox[2] / 2) / image_width
                y_center = (bbox[1] + bbox[3] / 2) / image_height
                width = bbox[2] / image_width
                height = bbox[3] / image_height

                # 写入标签文件
                f.write(f"{category_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

        processed_count += 1
        if processed_count % 100 == 0:
            print(f"已处理 {processed_count} 张图像...")

    print(f"转换完成! 共处理 {processed_count} 张图像")
    print(f"图像保存在: {output_img_dir}")
    print(f"标签保存在: {output_label_dir}")

    # 创建类别文件在上一级目录
    classes_file = os.path.join(os.path.dirname(output_label_dir), 'classes.txt')
    with open(classes_file, 'w', encoding='utf-8') as f:
        for cat_id, cat_name in sorted(categories.items()):
            f.write(f"{cat_name}\n")

    print(f"类别文件已创建: {classes_file}")


def validate_conversion(output_label_dir, output_img_dir):
    """
    验证转换结果
    """
    print("\n验证转换结果...")

    # 检查标签文件
    label_files = list(Path(output_label_dir).glob("*.txt"))
    image_files = list(Path(output_img_dir).glob("*"))

    print(f"标签文件数量: {len(label_files)}")
    print(f"图像文件数量: {len(image_files)}")

    # 检查几个样本
    sample_count = min(3, len(label_files))
    for i in range(sample_count):
        label_file = label_files[i]
        print(f"\n样本 {i + 1}: {label_file.name}")

        with open(label_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for j, line in enumerate(lines):
                parts = line.strip().split()
                if len(parts) == 5:
                    class_id, x_center, y_center, width, height = parts
                    print(f"  目标 {j + 1}: 类别={class_id}, 中心=({x_center}, {y_center}), 尺寸=({width}, {height})")


if __name__ == "__main__":
    # 配置路径
    paddle_label_path = r'C:\Users\leon\Downloads\annotations\annotations\test.json'
    paddle_img_dir = r'C:\Users\leon\Downloads\annotations\images'

    output_img_dir = r'C:\Users\leon\Downloads\annotations\yolo\test\images'
    output_label_dir = r'C:\Users\leon\Downloads\annotations\yolo\test\labels'

    # 执行转换
    convert_paddle_to_yolo(paddle_label_path, paddle_img_dir, output_img_dir, output_label_dir)

    # 验证结果
    validate_conversion(output_label_dir, output_img_dir)