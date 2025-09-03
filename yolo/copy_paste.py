import os
import cv2
import random

# ========================
# 工具函数
# ========================
def yolo_to_xyxy(box, img_w, img_h):
    cls, x, y, w, h = box
    x1 = int((x - w / 2) * img_w)
    y1 = int((y - h / 2) * img_h)
    x2 = int((x + w / 2) * img_w)
    y2 = int((y + h / 2) * img_h)
    return int(cls), x1, y1, x2, y2

def xyxy_to_yolo(cls, x1, y1, x2, y2, img_w, img_h):
    w = (x2 - x1) / img_w
    h = (y2 - y1) / img_h
    x = (x1 + x2) / 2 / img_w
    y = (y1 + y2) / 2 / img_h
    return f"{cls} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n"

def boxes_overlap(box1, box2):
    """检查两个矩形是否重叠"""
    x1, y1, x2, y2 = box1
    xx1 = max(x1, box2[0])
    yy1 = max(y1, box2[1])
    xx2 = min(x2, box2[2])
    yy2 = min(y2, box2[3])
    return (xx2 - xx1) > 0 and (yy2 - yy1) > 0

# ========================
# Copy-Paste 核心函数
# ========================
def copy_paste_group(img_paths, label_paths,
                     out_img_path, out_label_path,
                     source_classes, copy_classes,
                     target_size=640, max_objects=15):
    """
    从多张图里取对象 -> 合成一张背景
    """
    bg = 114 * (np.ones((target_size, target_size, 3), dtype=np.uint8))  # 白色背景
    bg_h, bg_w = bg.shape[:2]
    new_labels = []
    placed_boxes = []

    for src_img_path, src_label_path in zip(img_paths, label_paths):
        src_img = cv2.imread(src_img_path)
        if src_img is None:
            continue
        h, w = src_img.shape[:2]

        with open(src_label_path, "r") as f:
            boxes = [list(map(float, line.strip().split())) for line in f]

        for box in boxes:
            if len(box) == 0:
                continue  # 跳过没有目标的标签
            cls, x1, y1, x2, y2 = yolo_to_xyxy(box, w, h)
            if cls not in source_classes or cls not in copy_classes:
                continue

            obj = src_img[y1:y2, x1:x2]
            if obj.size == 0:
                continue

            # 随机缩放
            scale = random.uniform(0.5, 1.0)
            nh, nw = int(obj.shape[0] * scale), int(obj.shape[1] * scale)
            if nh < 5 or nw < 5:
                continue
            obj = cv2.resize(obj, (nw, nh))

            # 找到不与已有 box 重叠的位置
            for _ in range(30):  # 尝试 30 次
                x_off = random.randint(0, bg_w - nw)
                y_off = random.randint(0, bg_h - nh)
                candidate_box = (x_off, y_off, x_off + nw, y_off + nh)

                if all(not boxes_overlap(candidate_box, b) for b in placed_boxes):
                    # 粘贴
                    bg[y_off:y_off + nh, x_off:x_off + nw] = obj
                    placed_boxes.append(candidate_box)

                    # 写标签
                    new_labels.append(
                        xyxy_to_yolo(cls, *candidate_box, bg_w, bg_h)
                    )
                    break

            if len(new_labels) >= max_objects:
                break
        if len(new_labels) >= max_objects:
            break

    # 保存结果
    cv2.imwrite(out_img_path, bg)
    with open(out_label_path, "w") as f:
        f.writelines(new_labels)


# ========================
# 主流程：随机 3~4 张图组合
# ========================
import numpy as np

def generate_dataset(img_dir, label_dir, out_dir,
                     source_classes, copy_classes,
                     num_groups=10):
    img_files = sorted([f for f in os.listdir(img_dir) if f.endswith(".jpg")])
    label_files = sorted([f for f in os.listdir(label_dir) if f.endswith(".txt")])

    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(os.path.join(out_dir, 'images'), exist_ok=True)
    os.makedirs(os.path.join(out_dir, 'labels'), exist_ok=True)

    for gid in range(num_groups):
        group_size = random.randint(3, 4)
        idxs = random.sample(range(len(img_files)), group_size)

        img_paths = [os.path.join(img_dir, img_files[i]) for i in idxs]
        label_paths = [os.path.join(label_dir, label_files[i]) for i in idxs]

        out_img_path = os.path.join(out_dir,'images', f"group_{gid}.jpg")
        out_label_path = os.path.join(out_dir,'labels', f"group_{gid}.txt")

        copy_paste_group(img_paths, label_paths,
                         out_img_path, out_label_path,
                         source_classes, copy_classes)


# ========================
# 示例调用
# ========================
class_map = {
    "person":0,
    "hat":1,
    "head":2,
    "reflectiveJacket":3,
    "hand":4,
    "ladder":5
}
if __name__ == "__main__":
    generate_dataset(
        img_dir=r"E:\dataSet\ymj_yolo_data\yolodata\person-hat-head\train\images",
        label_dir=r"E:\dataSet\ymj_yolo_data\yolodata\person-hat-head\train\labels_class_5",
        out_dir="reflectiveJacket_cp",
        source_classes = [class_map[c] for c in ['person','hat','head','reflectiveJacket',"hand","ladder"]],   # 假设所有类都能作为来源
        copy_classes   = [class_map[c] for c in ['hat']],           # 只粘贴某些类
        num_groups=2000                   # 生成多少组
    )
