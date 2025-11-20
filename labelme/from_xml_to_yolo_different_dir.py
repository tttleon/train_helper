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

# 图片和XML文件所在的子目录
img_subdir = 'JPEGImages'
xml_subdir = 'Annotations'

# 创建目标目录
os.makedirs(os.path.join(target_dir, 'images'), exist_ok=True)
os.makedirs(os.path.join(target_dir, 'labels'), exist_ok=True)

# 构建完整的路径
img_dir = os.path.join(source_dir, img_subdir)
xml_dir = os.path.join(source_dir, xml_subdir)

# 检查目录是否存在
if not os.path.exists(img_dir):
    print(f"错误: 图片目录不存在: {img_dir}")
    exit(1)
if not os.path.exists(xml_dir):
    print(f"错误: XML目录不存在: {xml_dir}")
    exit(1)

for xml_file in os.listdir(xml_dir):
    if xml_file.lower().endswith(".xml"):
        xml_path = os.path.join(xml_dir, xml_file)
        img_name = os.path.splitext(xml_file)[0]

        # 在图片目录中找对应的图片
        img_file = None
        for ext in img_exts:
            candidate = img_name + ext
            candidate_path = os.path.join(img_dir, candidate)
            if os.path.exists(candidate_path):
                img_file = candidate
                break

        if img_file is None:
            print(f"警告: 未找到图片文件 {img_name}，跳过")
            continue  # 没有对应图片则跳过

        # 解析 XML
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
        except Exception as e:
            print(f"警告: 解析XML文件 {xml_file} 时出错: {e}，跳过")
            continue

        size = root.find("size")
        if size is None:
            print(f"警告: XML文件 {xml_file} 中没有size信息，跳过")
            continue

        try:
            w = int(size.find("width").text)
            h = int(size.find("height").text)
        except (AttributeError, ValueError) as e:
            print(f"警告: XML文件 {xml_file} 中尺寸信息无效，跳过")
            continue

        yolo_lines = []
        for obj in root.findall("object"):
            name_elem = obj.find("name")
            if name_elem is None or name_elem.text is None:
                continue

            name = name_elem.text.strip()
            if name not in class_names:
                continue

            cls_id = class_names.index(name)
            bndbox = obj.find("bndbox")
            if bndbox is None:
                continue

            try:
                xmin = float(bndbox.find("xmin").text)
                ymin = float(bndbox.find("ymin").text)
                xmax = float(bndbox.find("xmax").text)
                ymax = float(bndbox.find("ymax").text)
            except (AttributeError, ValueError) as e:
                print(f"警告: XML文件 {xml_file} 中边界框坐标无效，跳过此对象")
                continue

            # 转 YOLO 格式
            x_center = ((xmin + xmax) / 2) / w
            y_center = ((ymin + ymax) / 2) / h
            bw = (xmax - xmin) / w
            bh = (ymax - ymin) / h

            # 检查坐标是否在有效范围内
            if not (0 <= x_center <= 1 and 0 <= y_center <= 1 and 0 <= bw <= 1 and 0 <= bh <= 1):
                print(f"警告: XML文件 {xml_file} 中边界框坐标超出范围，跳过此对象")
                continue

            yolo_lines.append(f"{cls_id} {x_center:.6f} {y_center:.6f} {bw:.6f} {bh:.6f}")

        # 写 YOLO 标签
        if yolo_lines:  # 只有当有有效标签时才创建文件
            txt_path = os.path.join(target_dir, 'labels', img_name + ".txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write("\n".join(yolo_lines))

            # 复制图片
            img_source_path = os.path.join(img_dir, img_file)
            img_target_path = os.path.join(target_dir, 'images', img_file)
            shutil.copy2(img_source_path, img_target_path)
            print(f"处理完成: {img_file}")
        else:
            print(f"警告: XML文件 {xml_file} 中没有有效的对象，跳过")

print("转换完成")