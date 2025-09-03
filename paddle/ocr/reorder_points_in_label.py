import json
import os
import shutil

import numpy as np

def sort_points(points):
    """将四点按 左上, 右上, 右下, 左下 顺序排序"""
    pts = np.array(points, dtype=np.float32)
    rect = np.zeros((4, 2), dtype=np.float32)

    # 左上：x+y 最小
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]

    # 右下：x+y 最大
    rect[2] = pts[np.argmax(s)]

    # 右上：y-x 最小
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]

    # 左下：y-x 最大
    rect[3] = pts[np.argmax(diff)]

    return rect.tolist()

def reorder_points_in_label(label_file):
    new_lines = []

    with open(label_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            try:
                img_path, ann_str = line.split("\t", 1)
                anns = json.loads(ann_str)

                changed = False
                for ann in anns:
                    points = ann.get("points", [])
                    if len(points) == 4:
                        sorted_pts = sort_points(points)
                        ann["points"] = sorted_pts
                        changed = True

                if changed:
                    new_line = img_path + "\t" + json.dumps(anns, ensure_ascii=False)
                else:
                    new_line = line
                new_lines.append(new_line)

            except Exception as e:
                print(f"解析错误：{line[:50]}... 错误: {e}")
                new_lines.append(line)

    # 覆盖写回文件
    with open(label_file, "w", encoding="utf-8") as f:
        for l in new_lines:
            f.write(l + "\n")

if __name__ == "__main__":
    label_file = r"E:\dataSet\ocr\icon_test\ppocr_label\Label.txt"
    # 如果备份文件已存在，则删除
    if os.path.exists(label_file + ".bak"):
        os.remove(label_file + ".bak")
    # 备份原数据
    shutil.copy(label_file, label_file + ".bak")
    # 执行修改
    reorder_points_in_label(label_file)
    print("已完成重排序并写回到原文件。")
