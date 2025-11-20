"""
python 删除yolo object detect的部分标签

比如原标签有[a,b,c]

我指定删除[b]

只剩下a和c

例如
0 xx
1 xx
2 xx

删除之后只剩下
0 xx
2 xx
"""
import os

# 要处理的标签目录
label_dir = r"E:\dataSet\ymj_yolo_data\yolodata\ladders-0909-gs\output_frames2\labels"

# 需要删除的类别id（可以是多个）
remove_ids = {4}  # 删除 class_id = 1 (即 b)

for file in os.listdir(label_dir):
    if not file.endswith(".txt"):
        continue

    file_path = os.path.join(label_dir, file)

    with open(file_path, "r") as f:
        lines = f.readlines()

    # 过滤掉不要的类别
    new_lines = []
    for line in lines:
        parts = line.strip().split()
        if not parts:
            continue
        cls_id = int(parts[0])
        if cls_id not in remove_ids:
            new_lines.append(line)

    # 写回文件（覆盖原文件）
    with open(file_path, "w") as f:
        f.writelines(new_lines)
