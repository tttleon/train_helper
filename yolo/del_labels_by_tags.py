"""
删除标签文件里面指定类比的标签

例如标签文件
1 0.8618113912231559 0.5216753368013872 0.06669334400426825 0.22675736961451257
0 0.18654128317993865 0.6528389133431151 0.17340269441109776 0.6491485483082121
2 0.8618113912231559 0.5216753368013872 0.06669334400426825 0.22675736961451257

删除 类别ID 为 2,3,4,5,6 的标签

删除之后的文件应该为
0 0.18654128317993865 0.6528389133431151 0.17340269441109776 0.6491485483082121

"""
import os

# ================= 配置区域 =================
label_dir_arr = [
    r'E:\dataSet\ymj_yolo_data\yolodata\ARDS-knif-pisto-rifle-stick\only_stick\train\labels',
    r'E:\dataSet\ymj_yolo_data\yolodata\ARDS-knif-pisto-rifle-stick\only_stick\valid\labels'
]

output_label_dir_arr = [
    r'E:\dataSet\ymj_yolo_data\yolodata\ARDS-knif-pisto-rifle-stick\only_stick\train\labels_del',
    r'E:\dataSet\ymj_yolo_data\yolodata\ARDS-knif-pisto-rifle-stick\only_stick\valid\labels_del'
]

# 需要删除的类别 ID 列表
del_id_arr = [1, 2, 3, 4, 5, 6]


# ================= 处理逻辑 =================

def filter_labels():
    # 将删除列表转换为字符串集合，便于后续快速比对 (防止文件中ID带有空格等格式问题)
    del_ids_set = set(str(x) for x in del_id_arr)

    # 遍历输入目录和输出目录
    for input_dir, output_dir in zip(label_dir_arr, output_label_dir_arr):

        # 1. 确保输出目录存在
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"已创建输出目录: {output_dir}")

        # 获取该目录下所有txt文件
        files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]

        print(f"正在处理目录: {input_dir} (共 {len(files)} 个文件)...")

        count_processed = 0

        for filename in files:
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            new_lines = []

            # 2. 读取原文件
            with open(input_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # 3. 逐行检查
            for line in lines:
                line = line.strip()
                if not line:
                    continue

                parts = line.split()
                if len(parts) > 0:
                    class_id = parts[0]

                    # 如果该行的 class_id 不在删除列表中，则保留
                    if class_id not in del_ids_set:
                        new_lines.append(line + '\n')

            # 4. 写入新文件
            # 即使 new_lines 为空（该图片所有标签都被删除了），也要生成一个空文件，
            # 否则 YOLO 训练时会报错找不到标签文件。
            with open(output_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)

            count_processed += 1

        print(f"完成! 已保存至: {output_dir}\n")


if __name__ == '__main__':
    print("--- 开始处理标签文件 ---")
    try:
        filter_labels()
        print("--- 所有任务处理完毕 ---")
    except Exception as e:
        print(f"发生错误: {e}")