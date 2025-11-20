"""
python 脚本，读取标签文件
标签文件的命名方式如下
32-frame_003910.jpg
32-frame_003920.jpg
。。。。。。

判断
如果标签文件的尾号数字大于等于003980
则把标签文件里面的 id为的3标签 改成 id 为2
"""

import os
import glob


def modify_labels_in_directory(directory_path):
    """
    修改指定目录中符合条件的标签文件
    将文件名尾号 >= 003980 的文件中的类别ID 3改为2
    """

    # 获取目录中所有的标签文件（假设是.txt文件）
    label_files = glob.glob(os.path.join(directory_path, "*.txt"))

    modified_count = 0

    for label_file in label_files:
        # 从文件名中提取数字部分
        filename = os.path.basename(label_file)

        # 提取数字部分（假设文件名格式为：32-frame_003910.txt）
        try:
            # 去掉扩展名，然后从下划线后提取数字
            number_part = filename.replace('.txt', '').split('_')[-1]
            file_number = int(number_part)
        except (ValueError, IndexError):
            print(f"跳过文件 {filename} - 文件名格式不符合预期")
            continue

        # 检查文件数字是否 >= 3980
        if file_number >= 3980:
            print(f"处理文件: {filename} (数字: {file_number})")

            # 读取文件内容
            with open(label_file, 'r') as f:
                lines = f.readlines()

            # 修改内容
            modified_lines = []
            changes_made = 0

            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 1:
                    # 检查类别ID是否为3
                    if parts[0] == '3':
                        parts[0] = '2'  # 将ID从3改为2
                        changes_made += 1
                    modified_lines.append(' '.join(parts))

            # 如果有修改，写回文件
            if changes_made > 0:
                with open(label_file, 'w') as f:
                    for line in modified_lines:
                        f.write(line + '\n')
                print(f"  修改了 {changes_made} 个标签")
                modified_count += 1
            else:
                print(f"  未找到需要修改的标签")

    print(f"\n处理完成！共修改了 {modified_count} 个文件")


def modify_specific_labels(directory_path, target_id=3, new_id=2, threshold=3980):
    """
    更通用的函数，可以指定不同的参数

    参数:
    - directory_path: 标签文件所在目录
    - target_id: 需要修改的目标ID
    - new_id: 修改后的新ID
    - threshold: 文件名数字阈值
    """

    label_files = glob.glob(os.path.join(directory_path, "*.txt"))
    modified_count = 0

    for label_file in label_files:
        filename = os.path.basename(label_file)

        try:
            number_part = filename.replace('.txt', '').split('_')[-1]
            file_number = int(number_part)
        except (ValueError, IndexError):
            continue

        if file_number >= threshold:
            with open(label_file, 'r') as f:
                lines = f.readlines()

            modified_lines = []
            changes_made = 0

            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 1 and parts[0] == str(target_id):
                    parts[0] = str(new_id)
                    changes_made += 1
                modified_lines.append(' '.join(parts))

            if changes_made > 0:
                with open(label_file, 'w') as f:
                    for line in modified_lines:
                        f.write(line + '\n')
                print(f"文件 {filename}: 将 {changes_made} 个ID从{target_id}改为{new_id}")
                modified_count += 1

    print(f"\n完成！在 {modified_count} 个文件中修改了标签")


# 使用方法
if __name__ == "__main__":
    # 指定包含标签文件的目录路径
    labels_directory = r"E:\dataSet\ymj_yolo_data\yolodata\hook-test-2025-11-3-behind\labels"  # 请修改为您的实际目录路径

    if os.path.exists(labels_directory):
        print("开始处理标签文件...")
        modify_specific_labels(labels_directory, target_id=3, new_id=2, threshold=1850)

        # 或者使用第一个函数
        # modify_labels_in_directory(labels_directory)
    else:
        print(f"目录 {labels_directory} 不存在，请检查路径")