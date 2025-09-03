'''
直接展示excel里面的标签框结果
'''
import cv2
import json
import os

import numpy as np

# 原始数据
boxjson = '{"meta":{},"id":"bdbf413a-2b41-4049-a5e1-28c3ec165513","items":[{"meta":{"rectStartPointerXY":[1879,1967],"pointRatio":0.5,"geometry":[1485,1524,1879,1967],"type":"BBOX"},"id":"05b3aa01-1ee0-4932-b8ef-aaf6833df6f5","properties":{"create_time":1620612621268,"accept_meta":{},"mark_by":"LABEL","is_system_map":false},"labels":{"标签":"wrongglove"}},{"meta":{"rectStartPointerXY":[975,990],"pointRatio":0.5,"geometry":[975,990,1603,1310],"type":"BBOX"},"id":"5d102e66-4a39-4918-9b8d-b74ebad6e5a2","properties":{"create_time":1620612633404,"accept_meta":{},"mark_by":"LABEL","is_system_map":false},"labels":{"标签":"glove"}},{"meta":{"rectStartPointerXY":[786,35],"pointRatio":0.5,"geometry":[896.65,0,2243,4000],"type":"BBOX"},"id":"c7f78d79-6453-4fb2-8a13-b78f67a38bf3","properties":{"create_time":1620612641675,"accept_meta":{},"mark_by":"LABEL","is_system_map":false},"labels":{"标签":"person"}}],"properties":{"seq":"964"},"labels":{"invalid":"false"},"timestamp":1620612654000}'

image_name = "c44ed365_f51d_424c_ae8e_f935834ec9bd.jpg"
image_path = r'E:\dataSet\ymj_yolo_data\yolodata\监护袖章、绝缘手套、人、监护袖章、未佩戴绝缘手套、操作杆、验电笔\train\images'



# 加载图像
full_image_path = os.path.join(image_path, image_name)
image = cv2.imread(full_image_path)

if image is None:
    raise FileNotFoundError(f"Image not found: {full_image_path}")

# 解析 JSON
data = json.loads(boxjson)

# 设置颜色映射
color_map = {
    "person": (0, 255, 0),
    "glove": (255, 0, 0),
    "wrongglove": (0, 0, 255)
}

# 遍历框
for item in data['items']:
    geometry = item['meta']['geometry']
    x1, y1, x2, y2 = map(int, geometry)
    label = item['labels'].get("标签", "unknown")
    color = color_map.get(label, (255, 255, 255))

    # 画矩形框
    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

    # 显示标签
    cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

# 保存到当前路径图像
cv2.imwrite("output_image.jpg", image)
