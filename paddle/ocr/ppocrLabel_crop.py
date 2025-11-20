import cv2
import numpy as np
import os
import json

def process_from_label(txt_file, save_dir, crop_size=640):
    os.makedirs(save_dir, exist_ok=True)

    with open(txt_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 文件路径 + json 部分
        try:
            img_path, json_str = line.split("\t", 1)
        except ValueError:
            print(f"行格式错误: {line}")
            continue

        # 加载标注
        try:
            annotations = json.loads(json_str)
        except json.JSONDecodeError:
            print(f"JSON 解析错误: {line}")
            continue

        # 收集所有点
        dt_polys = [np.array(anno["points"], dtype=np.int32) for anno in annotations]

        if not dt_polys:
            print(f"{img_path} 没有标注点，跳过")
            continue

        # 计算所有标注点的外接矩形
        all_points = np.vstack(dt_polys)
        x, y, w, h = cv2.boundingRect(all_points)
        cx, cy = x + w // 2, y + h // 2

        half = crop_size // 2

        # 读取原图
        img = cv2.imread(img_path)
        if img is None:
            print(f"图片读取失败: {img_path}")
            continue

        H, W = img.shape[:2]

        # 确保裁剪区域不越界
        x1 = max(0, cx - half)
        y1 = max(0, cy - half)
        x2 = min(W, cx + half)
        y2 = min(H, cy + half)

        crop = img[y1:y2, x1:x2]

        # padding 到 crop_size
        if crop.shape[0] != crop_size or crop.shape[1] != crop_size:
            padded = np.zeros((crop_size, crop_size, 3), dtype=np.uint8)
            padded[:crop.shape[0], :crop.shape[1]] = crop
            crop = padded

        # 保存
        filename = os.path.basename(img_path)
        save_path = os.path.join(save_dir, filename)
        cv2.imwrite(save_path, crop)


if __name__ == "__main__":
    txt_file = r"E:\dataSet\ocr\mcc_icon\train_data\det\train.txt"
    save_dir = "crop_640_from_label"
    crop_size = 640
    process_from_label(txt_file, save_dir, crop_size)
