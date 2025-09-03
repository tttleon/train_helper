import shutil
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

for d in dirs:
    if os.path.exists(d):
        shutil.rmtree(d)
        print(f"已删除目录: {d}")
    else:
        print(f"目录不存在: {d}")
