"""
从已经有的yolo数据集中提取指定百分比数量的数据
"""

import os
import shutil
import random

def extract_yolo_dataset(yolo_img_dir, yolo_label_dir, output_img_dir, output_label_dir, percent=0.1):
    """
    从YOLO数据集中提取指定百分比的数据
    
    Args:
        yolo_img_dir: 原始图片目录路径
        yolo_label_dir: 原始标签目录路径  
        output_img_dir: 输出图片目录路径
        output_label_dir: 输出标签目录路径
        percent: 提取百分比 (0.0-1.0)
    """
    
    # 创建输出目录
    os.makedirs(output_img_dir, exist_ok=True)
    os.makedirs(output_label_dir, exist_ok=True)
    
    # 获取所有图片文件（支持常见图片格式）
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
    image_files = []
    
    for file in os.listdir(yolo_img_dir):
        if any(file.lower().endswith(ext) for ext in image_extensions):
            image_files.append(file)
    
    print(f"找到 {len(image_files)} 个图片文件")
    
    # 随机打乱文件列表
    random.shuffle(image_files)
    
    # 计算需要提取的数量
    extract_count = int(len(image_files) * percent)
    print(f"需要提取 {extract_count} 个样本 ({percent*100}%)")
    
    # 提取文件
    extracted_files = image_files[:extract_count]
    
    success_count = 0
    for img_file in extracted_files:
        try:
            # 获取文件名（不含扩展名）
            filename = os.path.splitext(img_file)[0]
            
            # 复制图片文件
            img_src_path = os.path.join(yolo_img_dir, img_file)
            img_dst_path = os.path.join(output_img_dir, img_file)
            shutil.copy2(img_src_path, img_dst_path)
            
            # 查找对应的标签文件
            label_extensions = ['.txt']
            label_found = False
            
            for ext in label_extensions:
                label_file = filename + ext
                label_src_path = os.path.join(yolo_label_dir, label_file)
                
                if os.path.exists(label_src_path):
                    # 复制标签文件
                    label_dst_path = os.path.join(output_label_dir, label_file)
                    shutil.copy2(label_src_path, label_dst_path)
                    label_found = True
                    break
            
            if label_found:
                success_count += 1
            else:
                print(f"警告: 未找到 {img_file} 对应的标签文件")
                
        except Exception as e:
            print(f"错误: 处理文件 {img_file} 时出错: {e}")
    
    print(f"成功提取 {success_count} 个样本")
    print(f"输出目录: {output_img_dir}")
    print(f"标签目录: {output_label_dir}")

if __name__ == "__main__":
    # 使用你提供的路径
    yolo_img_dir = r"E:\dataSet\ymj_yolo_data\yolodata\person-hat-head\train\images"
    yolo_label_dir = r'E:\dataSet\ymj_yolo_data\yolodata\person-hat-head\train\labels-person-hat-head'
    output_img_dir = r"E:\dataSet\ymj_yolo_data\yolodata\person-hat-head\train_20\images"
    output_label_dir = r"E:\dataSet\ymj_yolo_data\yolodata\person-hat-head\train_20\labels-person-hat-head"
    percent = 0.2
    
    # 执行提取
    extract_yolo_dataset(yolo_img_dir, yolo_label_dir, output_img_dir, output_label_dir, percent)