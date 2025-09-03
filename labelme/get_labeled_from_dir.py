"""
从指定目录获取所有标注过的文件,复制粘贴到另一个目录
"""

source_dir = r'E:\work_important\新样本\20250815'
output_dir = r'E:\work_important\新样本\20250815-labeled'

# 获取所有的图片文件，如果其有对应的xml文件，则复制图片和xml文件到输出目录
# 例如 a.jpg 有 a.xml 则复制 a.jpg 和 a.xml


import os
import shutil

os.makedirs(output_dir, exist_ok=True)

# 支持的图片扩展名
img_exts = {".jpg", ".jpeg", ".png",".JPG", ".PNG", ".JPEG"}

for file in os.listdir(source_dir):
    name, ext = os.path.splitext(file)
    if ext.lower() in img_exts:
        xml_file = name + ".xml"
        xml_path = os.path.join(source_dir, xml_file)
        if os.path.exists(xml_path):
            # 复制图片和 xml
            shutil.copy2(os.path.join(source_dir, file), output_dir)
            shutil.copy2(xml_path, output_dir)

print("完成")
