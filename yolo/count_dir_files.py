import os

# 要统计的目录列表
directories = [
    r'E:\dataSet\ymj_yolo_data\yolodata\powerchecker-glove-wrongglove-person-badge-operatingbar\train\images',
    r'E:\dataSet\ymj_yolo_data\yolodata\ladder-person\train\images',
    r'E:\dataSet\ymj_yolo_data\yolodata\helmet-reflectiveJacket\train\images',
    r'E:\dataSet\ymj_yolo_data\yolodata\fall-nonfall\train\images',
    r'E:\dataSet\ymj_yolo_data\yolodata\person-hat-head\train\images'
]

for dir_path in directories:
    if not os.path.isdir(dir_path):
        print(f"{dir_path} 不是一个有效的目录")
        continue

    file_count = 0
    for entry in os.listdir(dir_path):
        full_path = os.path.join(dir_path, entry)
        if os.path.isfile(full_path):
            file_count += 1

    print(f"{dir_path} 中有 {file_count} 个文件")
