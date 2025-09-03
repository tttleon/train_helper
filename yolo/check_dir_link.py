"""
检查软连接
"""
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

for d in dirs:
    label_dir = os.path.join(os.path.dirname(d), "labels")
    if os.path.exists(label_dir):
        if os.path.islink(label_dir):
            real_path = os.readlink(label_dir)
            print(f"{label_dir} -> {real_path}")
        else:
            print(f"{label_dir} 不是软链接")
    else:
        print(f"{label_dir} 不存在")
