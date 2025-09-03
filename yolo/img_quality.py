'''
分数越低越好

0~20：质量很高

20~40：中等

40：质量较差（可能有模糊、压缩、噪声等问题）
'''
import shutil

import cv2 as cv
import os

def get_brisque_score(image_path, model_path="./model/brisque_model_live.yml", range_path="./model/brisque_range_live.yml"):
    image = cv.imread(image_path)
    if image is None:
        print(f"读取失败：{image_path}")
        return None
    # 创建 BRISQUE 质量评估器
    brisque = cv.quality_QualityBRISQUE.create(model_path, range_path)
    # 返回分数（单元素列表），越低图像质量越高
    score = brisque.compute(image)[0]
    return score

# 测试：单张图
# score = get_brisque_score("img/bad.jpg")
# print(f"BRISQUE 评分: {score:.2f}")
dic =[]
dir =r"E:\dataSet\ymj_yolo_data\yolodata\helmet-reflectiveJacket\valid\images -test"
for file in os.listdir(dir):
    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
        file_path = os.path.join(dir, file)
        score = get_brisque_score(file_path)
        if score is not None:
            # print(f"{file}: BRISQUE 评分: {score:.2f}")
            dic.append({
                "file": file,
                "score": score
            })
        else:
            print(f"{file}: 读取失败或评分计算失败")

# 按评分排序
dic.sort(key=lambda x: x["score"])
# 打印
for item in dic:
    print(f"{item['file']}: BRISQUE 评分: {item['score']:.2f}")

# 按照梯度 0~100，没10个为一组，复制文件到新的目录 例如E:\dataSet\ymj_yolo_data\yolodata\helmet-reflectiveJacket\valid\images -test-10
for i in range(0, 100, 10):
    out_dir = os.path.join(dir, f"images-{i}-{i+10}")
    os.makedirs(out_dir, exist_ok=True)
    for item in dic:
        if i <= item["score"] < i + 10:
            src_file = os.path.join(dir, item["file"])
            dst_file = os.path.join(out_dir, item["file"])
            if not os.path.exists(dst_file):  # 避免重复复制
                shutil.copy(src_file, dst_file)
                print(f"复制 {item['file']} 到 {out_dir}")