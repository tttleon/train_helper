import json

def check_label_points(label_file):


    bad_images = []

    with open(label_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            try:
                # 每行格式： image_path \t [json]
                img_path, ann_str = line.split("\t", 1)
                anns = json.loads(ann_str)

                for ann in anns:
                    points = ann.get("points", [])
                    if len(points) != 4:  # 不是四点
                        bad_images.append(img_path)
                        break  # 这张图有问题就直接记下来，避免重复
            except Exception as e:
                print(f"解析错误：{line[:50]}...  错误信息: {e}")

    if bad_images:
        print("存在超过四点的标注：")
        for img in bad_images:
            print(img)
    else:
        print("所有数据 points 都是四点")

if __name__ == "__main__":
    label_file = r"E:\dataSet\ocr\icon_test\ppocr_label\Label.txt"
    check_label_points(label_file)


