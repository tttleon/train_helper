import os
import shutil
from pathlib import Path

def is_image(file_path):
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    return file_path.suffix.lower() in image_extensions

def get_unique_filename(dest_dir, file_name):
    name, ext = os.path.splitext(file_name)
    counter = 1
    new_name = file_name
    while os.path.exists(os.path.join(dest_dir, new_name)):
        new_name = f"{name}_{counter}{ext}"
        counter += 1
    return new_name

def copy_images_with_rename_recursive(src_dir, dest_dir):
    src_dir = Path(src_dir)
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    for root, _, files in os.walk(src_dir):
        for file in files:
            file_path = Path(root) / file
            if is_image(file_path):
                unique_name = get_unique_filename(dest_dir, file_path.name)
                shutil.copy2(file_path, dest_dir / unique_name)

# 示例用法：
copy_images_with_rename_recursive(r"E:\work_important\中冶钢铁\20250509", r"E:\dataSet\ocr\mcc_icon")
