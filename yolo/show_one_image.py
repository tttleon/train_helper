'''
直接展示一张图片和对应的标签文件
'''

import cv2
import os

import numpy as np



# 定义颜色映射，支持10个类别
color_map = {
    0: (0, 255, 0),    # 绿色
    1: (255, 0, 0),    # 蓝色
    2: (0, 0, 255),    # 红色
    3: (255, 255, 0),  # 青色
    4: (255, 0, 255),  # 品红
    5: (0, 255, 255),  # 黄色
    6: (128, 0, 128),  # 紫色
    7: (128, 128, 0),  # 橄榄色
    8: (0, 128, 128),  # 青绿色
    9: (128, 128, 128)   # 灰色
}


def showImage2(img_path, label_path):
    # 读取图像
    image = cv2.imread(img_path)
    height, width, _ = image.shape
    print(f"Image shape: {image.shape}")

    # 读取标签文件
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split()
                class_id = int(parts[0])
                x_center, y_center, w, h = map(float, parts[1:])

                print(f"x_center={x_center}")
                print(f"y_center={y_center}")

                # 还原边界框到图像坐标
                print(f"class_id={class_id}")

                x = int((x_center - w / 2) * width)
                y = int((y_center - h / 2) * height)
                w = int(w * width)
                h = int(h * height)

                print(x, y, w, h)

                # 画矩形框并标注类别
                cv2.rectangle(image, (x, y), (x + w, y + h), color_map[class_id], 20)
                cv2.putText(image, f"{coco_class_name[class_id]}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 4, color_map[class_id], 10)



    # 图片缩放到720p方便显示
    scale_factor = 720 / max(height, width)
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    resized_image = cv2.resize(image, (new_width, new_height))
    cv2.imshow("Image with Bounding Boxes", resized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



# 文件路径
# img_path = "output/images/wide_image-6.png"
# label_path = "output/labels/wide_image-6.txt"
# showImage(img_path, label_path)

img_path = r"/yolo/hand\group_0.jpg"
label_path = r"/yolo/hand\group_0.txt"
coco_class_name = ["glove", "wrongglove", "person"] # 替换为你的类别名称

showImage2(img_path, label_path)
