import os
import shutil

def change_yolo_classes(original_label_dir, output_label_dir, num_change):
    """
    改变yolo标签文件中的类别编号
    
    参数:
        original_label_dir: 原始标签目录
        output_label_dir: 新标签输出目录
        num_change: 类别编号改变规则列表
    """
    
    # 确保输出目录存在
    if not os.path.exists(output_label_dir):
        os.makedirs(output_label_dir)
    
    # 创建类别映射字典
    class_mapping = {item["old"]: item["new"] for item in num_change}
    
    # 统计信息
    total_files = 0
    changed_labels = 0
    
    # 遍历原始标签目录中的所有文件
    for filename in os.listdir(original_label_dir):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(original_label_dir, filename)
            output_file_path = os.path.join(output_label_dir, filename)
            
            total_files += 1
            
            try:
                with open(input_file_path, 'r', encoding='utf-8') as input_file:
                    lines = input_file.readlines()
                
                new_lines = []
                
                for line in lines:
                    line = line.strip()
                    if not line:  # 跳过空行
                        continue
                    
                    parts = line.split()
                    if len(parts) >= 5:  # YOLO格式: class x_center y_center width height
                        old_class = int(parts[0])
                        
                        # 检查是否需要改变类别
                        if old_class in class_mapping:
                            new_class = class_mapping[old_class]
                            parts[0] = str(new_class)
                            changed_labels += 1
                            new_line = ' '.join(parts)
                            new_lines.append(new_line)
                            print(f"文件 {filename}: 类别 {old_class} -> {new_class}")
                        else:
                            # 如果不需要改变，保持原样
                            new_lines.append(line)
                
                # 写入新的标签文件
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write('\n'.join(new_lines))
                
                print(f"处理完成: {filename}")
                
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {e}")
    
    print(f"\n处理完成!")
    print(f"总共处理文件数: {total_files}")
    print(f"改变的标签数量: {changed_labels}")

# 使用示例
if __name__ == "__main__":
    original_label_dir = r'E:\dataSet\ymj_yolo_data\yolodata\ARDS-knif-pisto-rifle-stick\only_stick\train\labels'
    output_label_dir = r'E:\dataSet\ymj_yolo_data\yolodata\ARDS-knif-pisto-rifle-stick\only_stick\train\labels-f'

    # 确保输出目录存在
    os.makedirs(output_label_dir, exist_ok=True)
    
    # 定义类别改变规则
    num_change = [
        {
            "old": 3,
            "new": 0
        }
    ]
    
    change_yolo_classes(original_label_dir, output_label_dir, num_change)