import os

dirs = [
    # train
    r'E:\dataSet\ymj_yolo_data\yolodata\person-hat-head\train\labels',
    r'E:\dataSet\ymj_yolo_data\yolodata\helmet-reflectiveJacket\train\labels',
    r'E:\dataSet\ymj_yolo_data\yolodata\Glove\train\labels',
    r'E:\dataSet\ymj_yolo_data\yolodata\Glove\train-arg\labels',
    r'E:\dataSet\ymj_yolo_data\yolodata\ladders-2\train\labels',
    r'E:\dataSet\ymj_yolo_data\yolodata\ladders-2\train-arg\labels',
    r'E:\dataSet\ymj_yolo_data\yolodata\ladder-dianxin\train\labels',
    r'E:\dataSet\ymj_yolo_data\yolodata\ladder-dianxin\train-arg\labels',
    r'E:\dataSet\ymj_yolo_data\yolodata\fall-haitu\train\labels',
    # valid
    r'E:\dataSet\ymj_yolo_data\yolodata\person-hat-head\valid\labels',
    r'E:\dataSet\ymj_yolo_data\yolodata\helmet-reflectiveJacket\valid\labels',
    r'E:\dataSet\ymj_yolo_data\yolodata\Glove\valid\labels',
    r'E:\dataSet\ymj_yolo_data\yolodata\Glove\valid-arg\labels',
    r'E:\dataSet\ymj_yolo_data\yolodata\ladders-2\valid\labels',
    r'E:\dataSet\ymj_yolo_data\yolodata\ladders-2\valid-arg\labels',
    r'E:\dataSet\ymj_yolo_data\yolodata\ladder-dianxin\valid\labels',
    r'E:\dataSet\ymj_yolo_data\yolodata\ladder-dianxin\valid-arg\labels',
    r'E:\dataSet\ymj_yolo_data\yolodata\fall-haitu\valid\labels',
    # 继续加 ...
]

new_link_name = "labels_class_10"
new_backup_name = "arg_class_old"
fake = False  # True: 只打印不执行，False: 真正执行

for d in dirs:
    base_dir = os.path.dirname(d)       # train 或 valid 的目录
    label_dir = os.path.join(base_dir, "labels")  # 当前 labels
    new_link_target = os.path.join(base_dir, new_link_name)  # 新软链接目标目录
    backup_dir = os.path.join(base_dir, new_backup_name)     # 备份目录

    if os.path.exists(label_dir):
        if os.path.islink(label_dir):
            # 如果是软链接
            print(f"[软链接] {label_dir} -> {os.readlink(label_dir)}")
            if not fake:
                os.unlink(label_dir)
                print(f"删除软链接: {label_dir}")
        else:
            # 如果是普通目录
            print(f"[目录] {label_dir}")
            if not fake:
                if os.path.exists(backup_dir):
                    print(f"备份目录已存在，跳过重命名: {backup_dir}")
                else:
                    os.rename(label_dir, backup_dir)
                    print(f"重命名 {label_dir} -> {backup_dir}")
    else:
        print(f"{label_dir} 不存在，跳过")
        continue

    # 创建新的软链接
    if os.path.exists(new_link_target):
        print(f"准备创建新软链接: {label_dir} -> {new_link_target}")
        if not fake:
            os.symlink(new_link_target, label_dir)
            print(f"创建新软链接: {label_dir} -> {new_link_target}")
    else:
        print(f"目标目录不存在，无法创建软链接: {new_link_target}")

    # 打印执行后结果
    if os.path.exists(label_dir):
        if os.path.islink(label_dir):
            print(f"[执行后] {label_dir} -> {os.readlink(label_dir)}")
        else:
            print(f"[执行后] {label_dir} 是普通目录")
    else:
        print(f"[执行后] {label_dir} 不存在")

    print("-" * 60)
