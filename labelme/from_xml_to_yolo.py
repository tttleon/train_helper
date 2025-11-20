"""
读取LabelMe的xml文件，转换为YOLO格式的txt文件，并且把图片和标签文件复制到指定目录下的images和labels。
例如 a.jpg,a.xml 转换为 yolo格式的a.txt , 然后把a.jpg复制到指定目录下的images文件夹，a.txt复制到指定目录下的labels文件夹。
"""
import os
import shutil
import xml.etree.ElementTree as ET

source_dir = r'C:\Users\leon\Downloads\抽烟手势'
target_dir = r'C:\Users\leon\Downloads\抽烟手势-yolo'
# class_names =  ['person','hat','head','reflectiveJacket',"hand","ladder",'fall']
# class_names =  ['box', 'ear', 'hook', 'hooked']
class_names =  ['smoke']
# 支持的图片扩展名
img_exts = {".jpg", ".jpeg", ".png",".JPG", ".PNG", ".JPEG",'webp'}

# 创建目标目录
os.makedirs(os.path.join(target_dir, 'images'), exist_ok=True)
os.makedirs(os.path.join(target_dir, 'labels'), exist_ok=True)

for file in os.listdir(source_dir):
    if file.lower().endswith(".xml"):
        xml_path = os.path.join(source_dir, file)
        img_name = os.path.splitext(file)[0]

        # 找对应的图片
        img_file = None
        for ext in img_exts:
            candidate = img_name + ext
            if os.path.exists(os.path.join(source_dir, candidate)):
                img_file = candidate
                break
        if img_file is None:
            continue  # 没有对应图片则跳过

        # 解析 XML
        tree = ET.parse(xml_path)
        root = tree.getroot()

        size = root.find("size")
        if size is None:
            continue
        w = int(size.find("width").text)
        h = int(size.find("height").text)

        yolo_lines = []
        for obj in root.findall("object"):
            name = obj.find("name").text.strip()
            if name not in class_names:
                continue
            cls_id = class_names.index(name)
            bndbox = obj.find("bndbox")
            if bndbox is None:
                continue

            xmin = float(bndbox.find("xmin").text)
            ymin = float(bndbox.find("ymin").text)
            xmax = float(bndbox.find("xmax").text)
            ymax = float(bndbox.find("ymax").text)

            # 转 YOLO 格式
            x_center = ((xmin + xmax) / 2) / w
            y_center = ((ymin + ymax) / 2) / h
            bw = (xmax - xmin) / w
            bh = (ymax - ymin) / h

            yolo_lines.append(f"{cls_id} {x_center:.6f} {y_center:.6f} {bw:.6f} {bh:.6f}")

        # 写 YOLO 标签
        txt_path = os.path.join(target_dir,'labels', img_name + ".txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(yolo_lines))

        # 复制图片和标签
        shutil.copy2(os.path.join(source_dir, img_file), os.path.join(target_dir, 'images'))

print("转换完成")