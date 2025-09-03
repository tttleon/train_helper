"""
分割格式转换成 yolov5的obejct detect 模式
"""
import os
import shutil

def is_yolo_format(line: str) -> bool:
    """
    判断一行是否是 YOLO bbox 格式 (class x_center y_center w h)
    """
    parts = line.strip().split()
    if len(parts) != 5:  # YOLO 格式每行 5 个数
        return False
    try:
        cls = int(parts[0])       # 第一个是整数
        floats = list(map(float, parts[1:]))  # 后四个是浮点数
        return True
    except ValueError:
        return False


def polygon_to_yolo_line(polygon_line: str):
    """
    把一行 polygon 标注转换为 YOLOv5 bbox 格式
    输入格式: class x1 y1 x2 y2 ...
    输出格式: class x_center y_center w h
    """
    data = list(map(float, polygon_line.strip().split()))
    cls = int(data[0])
    coords = data[1:]

    # 将点分组 [(x1,y1), (x2,y2), ...]
    points = [(coords[i], coords[i+1]) for i in range(0, len(coords), 2)]

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    # 外接矩形
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)

    # 转换成 YOLO: x_center, y_center, w, h
    x_center = (xmin + xmax) / 2
    y_center = (ymin + ymax) / 2
    w = xmax - xmin
    h = ymax - ymin

    return f"{cls} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}"


def convert_file(input_path: str, output_path: str):
    with open(input_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    # 如果文件已经是 YOLO 格式 → 直接复制
    if all(is_yolo_format(line) for line in lines):
        shutil.copy(input_path, output_path)
        print(f"已是 YOLO 格式, 复制: {input_path} -> {output_path}")
        return

    # 否则 → 转换 polygon → YOLO
    yolo_lines = [polygon_to_yolo_line(line) for line in lines]

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(yolo_lines))

    print(f"转换完成: {input_path} -> {output_path}")


def batch_convert(input_dir: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            convert_file(input_path, output_path)


if __name__ == "__main__":
    # 修改成你的标注文件夹路径
    input_dir = r"E:\dataSet\ymj_yolo_data\yolodata\fire-smoke\valid\labels-fire-smoke--have-seg"   # 原始标注文件夹
    output_dir = r"E:\dataSet\ymj_yolo_data\yolodata\fire-smoke\valid\labels-fire-smoke_box"     # 输出 YOLO 格式标注文件夹

    batch_convert(input_dir, output_dir)
