import os


def get_some_class_from_labels(label_dir,output_label_dir,need_class ):
    """
    从标签文件中获取指定的类别，然后保存到新的标签文件中
    所以id按照all_class的顺序来

    例如已有标签xxx.txt：
    ["glove", "hand", "person"]
    0 xx xx xx xx  // glove
    1 xx xx xx xx  // hand
    2 xx xx xx xx

    只需要
    ["glove", "hand"]

    索引顺序按照新的来
    ['personFall','personNotFall','hat','head','reflectiveJacket',"glove", "hand",'ladder']

    则最终输出标签xxx.txt：
    5 xx xx xx xx // glove
    6 xx xx xx xx // hand

    """
    # 创建类别名到新索引的映射
    class_to_new_index = {cls: idx for idx, cls in enumerate(all_class)}
    # 已有类别顺序（原始标签中使用的类别顺序）
    old_index_to_class = {idx: cls for idx, cls in enumerate(already_have_class)}

    for file_name in os.listdir(label_dir):
        if not file_name.endswith(".txt"):
            continue

        input_path = os.path.join(label_dir, file_name)
        output_path = os.path.join(output_label_dir, file_name)
        new_lines = []

        with open(input_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if not parts:
                    continue

                old_class_id = int(parts[0])
                class_name = old_index_to_class.get(old_class_id)

                if class_name in need_class:
                    new_class_id = class_to_new_index[class_name]
                    new_line = ' '.join([str(new_class_id)] + parts[1:])
                    new_lines.append(new_line)
        print(f"output_path={output_path}")
        with open(output_path, 'a') as f_out:
            # 判断文件是否为空，如果不是空的，就先写一个换行符
            if os.path.getsize(output_path) > 0:
                f_out.write('\n')
            f_out.write('\n'.join(new_lines))


# 最终输出的类别
all_class = ["people","fall","helmet","unhelmet","vest","novest","glove","no_glove","insulated_ladder","fire"]

# 自动打标模型中存在的类别，或者标签目录中已经存在的类别
already_have_class = ['unhelmet', 'people', 'no_glove', 'insulated_ladder', 'unwear']
                   # ['person','hat','head','reflectiveJacket',"hand","ladder",'glove','fall']

# 需要保留的类别
need_class = ['people','helmet','unhelmet','vest',"no_glove","insulated_ladder",'glove','fall']

# 多个已有标签目录
#    E:\dataSet\ymj_yolo_data\yolodata\Glove\train\images
#   - E:\dataSet\ymj_yolo_data\yolodata\Glove\train-arg\images
#   - E:\dataSet\ymj_yolo_data\yolodata\ladders-2\train\images
#   - E:\dataSet\ymj_yolo_data\yolodata\ladders-2\train-arg\images
#   - E:\dataSet\ymj_yolo_data\yolodata\ladder-dianxin\train\images
#   - E:\dataSet\ymj_yolo_data\yolodata\ladder-dianxin\train-arg\images
#   - E:\dataSet\ymj_yolo_data\yolodata\fall-haitu\train\images
label_dirs = [
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

# 多个输出标签目录
output_label_dirs = [
    # train
    r'E:\dataSet\ymj_yolo_data\yolodata\person-hat-head\train\labels_class_10',
    r'E:\dataSet\ymj_yolo_data\yolodata\helmet-reflectiveJacket\train\labels_class_10',
    r'E:\dataSet\ymj_yolo_data\yolodata\Glove\train\labels_class_10',
    r'E:\dataSet\ymj_yolo_data\yolodata\Glove\train-arg\labels_class_10',
    r'E:\dataSet\ymj_yolo_data\yolodata\ladders-2\train\labels_class_10',
    r'E:\dataSet\ymj_yolo_data\yolodata\ladders-2\train-arg\labels_class_10',
    r'E:\dataSet\ymj_yolo_data\yolodata\ladder-dianxin\train\labels_class_10',
    r'E:\dataSet\ymj_yolo_data\yolodata\ladder-dianxin\train-arg\labels_class_10',
    r'E:\dataSet\ymj_yolo_data\yolodata\fall-haitu\train\labels_class_10',
    # valid
    r'E:\dataSet\ymj_yolo_data\yolodata\person-hat-head\valid\labels_class_10',
    r'E:\dataSet\ymj_yolo_data\yolodata\helmet-reflectiveJacket\valid\labels_class_10',
    r'E:\dataSet\ymj_yolo_data\yolodata\Glove\valid\labels_class_10',
    r'E:\dataSet\ymj_yolo_data\yolodata\Glove\valid-arg\labels_class_10',
    r'E:\dataSet\ymj_yolo_data\yolodata\ladders-2\valid\labels_class_10',
    r'E:\dataSet\ymj_yolo_data\yolodata\ladders-2\valid-arg\labels_class_10',
    r'E:\dataSet\ymj_yolo_data\yolodata\ladder-dianxin\valid\labels_class_10',
    r'E:\dataSet\ymj_yolo_data\yolodata\ladder-dianxin\valid-arg\labels_class_10',
    r'E:\dataSet\ymj_yolo_data\yolodata\fall-haitu\valid\labels_class_10',
    # 继续加 ...
]



# main
if __name__ == "__main__":
    for label_dir, output_label_dir in zip(label_dirs, output_label_dirs):
        os.makedirs(output_label_dir, exist_ok=True)
        get_some_class_from_labels(label_dir, output_label_dir, need_class)