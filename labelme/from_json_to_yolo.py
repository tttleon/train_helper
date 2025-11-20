"""
读取LabelMe的xml文件，转换为YOLO格式的txt文件，并且把图片和标签文件复制到指定目录下的images和labels。
例如 a.jpg,a.xml 转换为 yolo格式的a.txt , 然后把a.jpg复制到指定目录下的images文件夹，a.txt复制到指定目录下的labels文件夹。
"""
import os
import shutil
import json

source_dir = r'E:\dataSet\ymj_yolo_data\yolodata\hook-test-2025-11-18-chiFeng\2661'
target_dir = r'E:\dataSet\ymj_yolo_data\yolodata\hook-test-2025-11-18-chiFeng\2661-yolo'
class_names = ['box', 'ear', 'hook', 'hooked']
# 支持的图片扩展名
img_exts = {".jpg", ".jpeg", ".png", ".JPG", ".PNG", ".JPEG", 'webp'}

# 创建目标目录
os.makedirs(os.path.join(target_dir, 'images'), exist_ok=True)
os.makedirs(os.path.join(target_dir, 'labels'), exist_ok=True)

for file in os.listdir(source_dir):
    if file.lower().endswith(".json"):
        json_path = os.path.join(source_dir, file)

        # 读取JSON文件
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"读取JSON文件失败: {json_path}, 错误: {e}")
            continue

        # 从JSON中获取图片文件名
        img_file_name = data.get("imagePath", "")
        if not img_file_name:
            # 如果JSON中没有imagePath，尝试用同名的图片文件
            img_name = os.path.splitext(file)[0]
            img_file = None
            for ext in img_exts:
                candidate = img_name + ext
                if os.path.exists(os.path.join(source_dir, candidate)):
                    img_file = candidate
                    break
            if img_file is None:
                print(f"未找到对应的图片文件: {img_name}")
                continue
        else:
            img_file = img_file_name
            # 检查图片文件是否存在
            if not os.path.exists(os.path.join(source_dir, img_file)):
                # 如果直接路径不存在，尝试在源目录中查找
                img_base_name = os.path.basename(img_file)
                if not os.path.exists(os.path.join(source_dir, img_base_name)):
                    print(f"图片文件不存在: {img_file}")
                    continue
                img_file = img_base_name

        # 获取图片尺寸
        img_height = data.get("imageHeight")
        img_width = data.get("imageWidth")
        if img_height is None or img_width is None:
            print(f"JSON文件中缺少图片尺寸信息: {json_path}")
            continue

        w = img_width
        h = img_height

        yolo_lines = []
        shapes = data.get("shapes", [])

        for shape in shapes:
            label = shape.get("label", "").strip()
            if label not in class_names:
                continue

            cls_id = class_names.index(label)
            points = shape.get("points", [])
            shape_type = shape.get("shape_type", "")

            # 只处理矩形标注
            if shape_type != "rectangle" or len(points) != 2:
                continue

            # 获取矩形框的两个点
            x1, y1 = points[0]
            x2, y2 = points[1]

            # 确保坐标顺序正确
            xmin = min(x1, x2)
            xmax = max(x1, x2)
            ymin = min(y1, y2)
            ymax = max(y1, y2)

            # 限制坐标在图片范围内
            xmin = max(0, min(xmin, w))
            xmax = max(0, min(xmax, w))
            ymin = max(0, min(ymin, h))
            ymax = max(0, min(ymax, h))

            # 转 YOLO 格式
            x_center = ((xmin + xmax) / 2) / w
            y_center = ((ymin + ymax) / 2) / h
            bw = (xmax - xmin) / w
            bh = (ymax - ymin) / h

            # 确保坐标在0-1范围内
            x_center = max(0, min(x_center, 1))
            y_center = max(0, min(y_center, 1))
            bw = max(0, min(bw, 1))
            bh = max(0, min(bh, 1))

            yolo_lines.append(f"{cls_id} {x_center:.6f} {y_center:.6f} {bw:.6f} {bh:.6f}")

        # 写 YOLO 标签
        img_name_without_ext = os.path.splitext(img_file)[0]
        txt_path = os.path.join(target_dir, 'labels', img_name_without_ext + ".txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(yolo_lines))

        # 复制图片
        src_img_path = os.path.join(source_dir, img_file)
        dst_img_path = os.path.join(target_dir, 'images', img_file)

        if os.path.exists(src_img_path):
            shutil.copy2(src_img_path, dst_img_path)
        else:
            print(f"图片文件不存在，无法复制: {src_img_path}")

print("转换完成")