import os

# 指定要清理缓存的目录列表
train_dirs = [
    r"E:\dataSet\ymj_yolo_data\yolodata\person-hat-head\train\images",
    r"E:\dataSet\ymj_yolo_data\yolodata\helmet-reflectiveJacket\train\images",
    r"E:\dataSet\ymj_yolo_data\yolodata\Glove\train\images",
    r"E:\dataSet\ymj_yolo_data\yolodata\Glove\train-arg\images",
    r"E:\dataSet\ymj_yolo_data\yolodata\ladders-2\train\images",
    r"E:\dataSet\ymj_yolo_data\yolodata\ladders-2\train-arg\images",
    r"E:\dataSet\ymj_yolo_data\yolodata\ladder-dianxin\train\images",
    r"E:\dataSet\ymj_yolo_data\yolodata\ladder-dianxin\train-arg\images",
    r"E:\dataSet\ymj_yolo_data\yolodata\fall-haitu\train\images"
]

val_dirs = [
    r"E:\dataSet\ymj_yolo_data\yolodata\person-hat-head\valid\images",
    r"E:\dataSet\ymj_yolo_data\yolodata\helmet-reflectiveJacket\valid\images",
    r"E:\dataSet\ymj_yolo_data\yolodata\Glove\valid\images",
    r"E:\dataSet\ymj_yolo_data\yolodata\Glove\valid-arg\images",
    r"E:\dataSet\ymj_yolo_data\yolodata\ladders-2\valid-arg\images",
    r"E:\dataSet\ymj_yolo_data\yolodata\ladders-2\valid\images",
    r"E:\dataSet\ymj_yolo_data\yolodata\ladder-dianxin\valid-arg\images",
    r"E:\dataSet\ymj_yolo_data\yolodata\ladder-dianxin\valid\images",
    r"E:\dataSet\ymj_yolo_data\yolodata\fall-haitu\valid\images"
    r'E:\dataSet\ymj_yolo_data\yolodata\fire-smoke\train\images',
    r'E:\dataSet\ymj_yolo_data\yolodata\fire-smoke\valid\images',
]

all_dirs = train_dirs + val_dirs

for img_dir in all_dirs:
    # YOLO 缓存文件一般在 images 目录的上一级或同级目录
    parent_dir = os.path.dirname(img_dir)

    for cache_name in ["labels.cache", "labels.cache.npy"]:
        cache_path = os.path.join(parent_dir, cache_name)
        if os.path.exists(cache_path):
            try:
                os.remove(cache_path)
                print(f"Deleted: {cache_path}")
            except Exception as e:
                print(f"Failed to delete {cache_path}: {e}")
        else:
            print(f"Not found: {cache_path}")
