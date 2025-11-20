'''
python脚本 E:\dataSet\ymj_yolo_data\yolodata\ladders-0909-gs\output_frames1
E:\dataSet\ymj_yolo_data\yolodata\ladders-0909-gs\output_frames2
这是两个目录，有相同的结构，里面都是images和labels，两个目录下面有重名的文件。
需要写个脚本合并这两个目录，复制粘贴到新的目录，并且重命名，并且对于image图片 和 label标签
'''
import os
import shutil

# 原始目录
dir1 = r"E:\dataSet\ymj_yolo_data\yolodata\ladders-0909-gs\output_frames1"
dir2 = r"E:\dataSet\ymj_yolo_data\yolodata\ladders-0909-gs\output_frames2"

# 新目录
merged_dir = r"E:\dataSet\ymj_yolo_data\yolodata\ladders-0909-gs\merged"
os.makedirs(merged_dir, exist_ok=True)
os.makedirs(os.path.join(merged_dir, "images"), exist_ok=True)
os.makedirs(os.path.join(merged_dir, "labels"), exist_ok=True)


def merge_dirs(source_dir, merged_dir, start_index=0):
    images_src = os.path.join(source_dir, "images")
    labels_src = os.path.join(source_dir, "labels")

    images_dst = os.path.join(merged_dir, "images")
    labels_dst = os.path.join(merged_dir, "labels")

    image_files = sorted(os.listdir(images_src))
    for i, img_file in enumerate(image_files, start=start_index):
        # 获取文件扩展名
        ext = os.path.splitext(img_file)[1]
        # 新文件名
        new_name = f"{i:06d}{ext}"

        # 复制 image
        shutil.copy(os.path.join(images_src, img_file), os.path.join(images_dst, new_name))

        # 复制对应 label
        label_file = os.path.splitext(img_file)[0] + ".txt"
        src_label_path = os.path.join(labels_src, label_file)
        if os.path.exists(src_label_path):
            shutil.copy(src_label_path, os.path.join(labels_dst, f"{i:06d}.txt"))

    return start_index + len(image_files)


# 合并两个目录
next_index = merge_dirs(dir1, merged_dir, start_index=0)
merge_dirs(dir2, merged_dir, start_index=next_index)

print("合并完成")
