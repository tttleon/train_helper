import os
from collections import defaultdict

# 标签目录列表
# labels_dirs = [
#     r'E:\dataSet\ymj_yolo_data\yolodata\person-hat-head\valid\labels',
#    r'E:\dataSet\ymj_yolo_data\yolodata\person-hat-head\train\labels',
#     r'E:\dataSet\ymj_yolo_data\yolodata\helmet-reflectiveJacket\valid\labels',
#     r'E:\dataSet\ymj_yolo_data\yolodata\helmet-reflectiveJacket\train\labels',
#     r'E:\dataSet\ymj_yolo_data\yolodata\Glove\train\labels',
#     r'E:\dataSet\ymj_yolo_data\yolodata\Glove\valid\labels',
#     r'E:\dataSet\ymj_yolo_data\yolodata\ladders-2\train-arg\labels',
#     r'E:\dataSet\ymj_yolo_data\yolodata\ladders-2\valid-arg\labels',
#     r'E:\dataSet\ymj_yolo_data\yolodata\ladder-dianxin\train-arg\labels',
#     r'E:\dataSet\ymj_yolo_data\yolodata\ladder-dianxin\valid-arg\labels',
#     r'E:\dataSet\ymj_yolo_data\yolodata\Glove\train-arg\labels',
#     r'E:\dataSet\ymj_yolo_data\yolodata\fall-haitu\train\labels',
#     r'E:\dataSet\ymj_yolo_data\yolodata\fall-haitu\valid\labels',
#     r'E:\dataSet\ymj_yolo_data\yolodata\fire-smoke\valid\labels',
#     r'E:\dataSet\ymj_yolo_data\yolodata\fire-smoke\train\labels',
# ]
# labels_dirs = [
#     r'E:\dataSet\ymj_yolo_data\yolodata\Glove\train\labels_class_7'
# ]
# train:
#   - E:\dataSet\ymj_yolo_data\yolodata\smoke-gesture-yolo\train\images
#   - E:\dataSet\ymj_yolo_data\yolodata\smoking-with-face\train\images
#   - E:\dataSet\ymj_yolo_data\yolodata\person-hat-head\train\images
# val:
#   - E:\dataSet\ymj_yolo_data\yolodata\smoke-gesture-yolo\valid\images
#   - E:\dataSet\ymj_yolo_data\yolodata\smoking-with-face\valid\images
#   - E:\dataSet\ymj_yolo_data\yolodata\person-hat-head\valid\images

labels_dirs =[
    r'E:\dataSet\ymj_yolo_data\yolodata\smoke-gesture-yolo\train\labels',
    # r'E:\dataSet\ymj_yolo_data\yolodata\smoking-with-face\train\labels',
    # r'E:\dataSet\ymj_yolo_data\yolodata\person-hat-head\train\labels',
    r'E:\dataSet\ymj_yolo_data\yolodata\person-hat-head\train_20\labels-person-hat-head'
]

# 所有类别（索引即为 class_id）
# all_class = ["people","fall","helmet","unhelmet","vest","novest","glove","no_glove","insulated_ladder","fire"]
all_class= ['person','hat','head','smoking']

# 初始化统计字典
class_counts = defaultdict(int)

total_file_count = 0

# 遍历目录和文件
for labels_dir in labels_dirs:
    for filename in os.listdir(labels_dir):
        total_file_count += 1
        file_path = os.path.join(labels_dir, filename)
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            with open(file_path, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if not parts:
                        continue
                    try:
                        class_id = int(parts[0])
                        if 0 <= class_id < len(all_class):
                            class_name = all_class[class_id]
                            class_counts[class_name] += 1
                    except ValueError:
                        continue  # 跳过无法解析为整数的行

# 打印统计结果
print("类别统计：")
for class_name in all_class:
    print(f"{class_name}: {class_counts[class_name]}")
# 打印总文件数
print(f"总文件数: {total_file_count}")


import matplotlib.pyplot as plt

# 筛选掉数量为 0 的类别
filtered_class_counts = {k: v for k, v in class_counts.items() if v > 0}

labels = list(filtered_class_counts.keys())
sizes = list(filtered_class_counts.values())

# 设置颜色（可选）
colors = plt.cm.tab20.colors  # 使用 tab20 colormap

# 绘制饼状图
plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors[:len(labels)], startangle=140)
plt.axis('equal')  # 保证饼图为圆形
plt.title('table')
plt.tight_layout()
plt.show()