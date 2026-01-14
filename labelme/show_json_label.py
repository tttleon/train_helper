import json
import os
import cv2
import numpy as np

# 配置参数
data_dir = r"E:\work_important\TC-re\TC-re-label\TC-re\test_img#251201\xiaomi"
out_dir = "./out"

# 创建输出目录（如果不存在）
os.makedirs(out_dir, exist_ok=True)

# 定义标签颜色映射（可根据需要调整）
label_colors = {
    "box": (0, 255, 0),  # 绿色
    "T": (0, 0, 255),  # 红色
    "C": (255, 0, 0),  # 蓝色
    "default": (255, 255, 0)  # 黄色（默认）
}


def draw_annotations(json_path, img_path, output_path):
    """
    解析JSON标注并绘制到图片上
    :param json_path: JSON标注文件路径
    :param img_path: 对应的图片路径
    :param output_path: 绘制后图片保存路径
    """
    # 读取JSON文件
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"读取JSON文件失败 {json_path}: {e}")
        return

    # 读取图片
    img = cv2.imread(img_path)
    if img is None:
        print(f"读取图片失败 {img_path}")
        return

    # 遍历所有标注形状
    for shape in data.get("shapes", []):
        label = shape.get("label", "")
        points = shape.get("points", [])
        shape_type = shape.get("shape_type", "")

        # 仅处理矩形标注
        if shape_type != "rectangle" or len(points) < 2:
            continue

        # 将浮点坐标转换为整数（OpenCV需要整数坐标）
        pt1 = (int(points[0][0]), int(points[0][1]))
        pt2 = (int(points[1][0]), int(points[1][1]))

        # 获取标签对应的颜色
        color = label_colors.get(label, label_colors["default"])

        # 绘制矩形框（线宽2）
        cv2.rectangle(img, pt1, pt2, color, 2)

        # 绘制标签文本（背景半透明）
        text = label
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8
        font_thickness = 2
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]

        # 文本位置（矩形左上角，避免超出图片）
        text_x = max(pt1[0], 10)
        text_y = max(pt1[1] - 10, text_size[1] + 10)

        # 绘制文本背景（半透明矩形）
        rect_pt1 = (text_x, text_y - text_size[1] - 5)
        rect_pt2 = (text_x + text_size[0] + 5, text_y + 5)
        overlay = img.copy()
        cv2.rectangle(overlay, rect_pt1, rect_pt2, color, -1)
        cv2.addWeighted(overlay, 0.5, img, 0.5, 0, img)

        # 绘制文本
        cv2.putText(img, text, (text_x + 2, text_y), font, font_scale, (255, 255, 255), font_thickness)

    # 保存绘制后的图片
    try:
        cv2.imwrite(output_path, img)
        print(f"保存成功: {output_path}")
    except Exception as e:
        print(f"保存图片失败 {output_path}: {e}")


# 遍历目录下所有JSON文件
for file_name in os.listdir(data_dir):
    # 筛选JSON文件
    if not file_name.lower().endswith(".json"):
        continue

    # 构建文件路径
    json_file = os.path.join(data_dir, file_name)
    # 匹配对应的图片文件（JSON文件名去掉.json，匹配相同前缀的图片）
    img_prefix = os.path.splitext(file_name)[0]
    img_file = None
    # 支持的图片格式
    img_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tif"]
    for ext in img_extensions:
        candidate = os.path.join(data_dir, img_prefix + ext)
        if os.path.exists(candidate):
            img_file = candidate
            break

    if img_file is None:
        print(f"未找到JSON {file_name} 对应的图片文件")
        continue

    # 构建输出文件路径
    out_file = os.path.join(out_dir, os.path.basename(img_file))
    # 绘制并保存
    draw_annotations(json_file, img_file, out_file)

print("所有文件处理完成！")