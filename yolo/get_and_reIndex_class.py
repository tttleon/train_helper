'''
把yolo数据集的标签文件中的类别重新索引为新的类别索引，并保存到新的标签文件中。

例如输入标签：
    ["powerchecker", "glove", "wrongglove", "person", "badge", "operatingbar"]
输出标签
   ["glove", "wrongglove", "person"]

将输出标签的索引重新映射为新的索引，不存在标签类别的类则删除，保存为新的标签文件。

'''

import os


def reindex_labels(input_dir, output_dir, input_classes, output_classes):
    """
    重新索引YOLO标签并保存为新的标签文件。

    参数：
        input_dir (str): 原始标签文件夹路径。
        output_dir (str): 新标签文件夹保存路径。
        input_classes (list of str): 所有原始类别名。
        output_classes (list of str): 需要保留并重新索引的类别名。
    """
    # 创建输出文件夹
    os.makedirs(output_dir, exist_ok=True)

    # 构建类别索引映射：原始索引 -> 新索引
    class_name_to_old_index = {name: i for i, name in enumerate(input_classes)}
    class_name_to_new_index = {name: i for i, name in enumerate(output_classes)}

    # 原始索引 -> 新索引 映射表
    old_index_to_new_index = {}
    for name in output_classes:
        if name in class_name_to_old_index:
            old_index = class_name_to_old_index[name]
            new_index = class_name_to_new_index[name]
            old_index_to_new_index[old_index] = new_index

    # 遍历标签文件
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            with open(input_path, 'r') as f:
                lines = f.readlines()

            new_lines = []
            for line in lines:
                parts = line.strip().split()
                if not parts:
                    continue
                class_id = int(parts[0])
                if class_id in old_index_to_new_index:
                    new_class_id = old_index_to_new_index[class_id]
                    new_line = " ".join([str(new_class_id)] + parts[1:]) + '\n'
                    new_lines.append(new_line)


            with open(output_path, 'w') as f:
                f.writelines(new_lines)

# 使用示例：
input_classes = ["powerchecker", "glove", "wrongglove", "person", "badge", "operatingbar"]
output_classes = ["glove", "wrongglove", "person"]
path_to_old_labels = r"E:\dataSet\ymj_yolo_data\yolodata\监护袖章、绝缘手套、人、监护袖章、未佩戴绝缘手套、操作杆、验电笔\train\labels-original-c6"  # 替换为你的原始标签文件夹路径
path_to_new_labels = r"E:\dataSet\ymj_yolo_data\yolodata\监护袖章、绝缘手套、人、监护袖章、未佩戴绝缘手套、操作杆、验电笔\train\labels"  # 替换为你希望保存新标签的文件夹路径

reindex_labels(path_to_old_labels, path_to_new_labels, input_classes, output_classes)

