'''
把飞桨数据集的csv格式转换为YOLO格式的标签格式
飞桨.xlsx格式:
    E列是图片：1_images/3862f096_1f70_4199_9300_c9cbb2b9075e.JPG
    F列是标签框的json：{"meta":{},"id":"03966586-56e9-40d8-adaf-84ccaf57d0e2","items":[{"meta":{"rectStartPointerXY":[2486,2312],"pointRatio":0.5,"geometry":[2486,2312,2648,2506],"type":"BBOX"},"id":"a2ca6226-711d-4e66-9ed3-4d48016634ba","properties":{"create_time":1620527316105,"accept_meta":{},"mark_by":"LABEL","is_system_map":false},"labels":{"标签":"wrongglove"}},{"meta":{"rectStartPointerXY":[2550,2301],"pointRatio":0.5,"geometry":[2550,2298,2672,2470],"type":"BBOX"},"id":"8bfc7aee-5db9-4cc8-9f1f-80a9fa921c18","properties":{"create_time":1620527324381,"accept_meta":{},"mark_by":"LABEL","is_system_map":false},"labels":{"标签":"wrongglove"}},{"meta":{"rectStartPointerXY":[2145,2089],"pointRatio":0.5,"geometry":[2145,2089,2742,4000],"type":"BBOX"},"id":"20f31a1a-a56e-4e66-a6dd-1fa46436b817","properties":{"create_time":1620527341180,"accept_meta":{},"mark_by":"LABEL","is_system_map":false},"labels":{"标签":"person"}},{"meta":{"rectStartPointerXY":[4501,2591],"pointRatio":0.5,"geometry":[4394,2402,4501,2591],"type":"BBOX"},"id":"07995493-ead5-40b9-9396-1da3a913433b","properties":{"create_time":1620527352060,"accept_meta":{},"mark_by":"LABEL","is_system_map":false},"labels":{"标签":"wrongglove"}},{"meta":{"rectStartPointerXY":[3908,2089],"pointRatio":0.5,"geometry":[3908,2082,4790,3993],"type":"BBOX"},"id":"7aa68511-ee79-4708-8821-2685d06c6c38","properties":{"create_time":1620527365884,"accept_meta":{},"mark_by":"LABEL","is_system_map":false},"labels":{"标签":"person"}},{"meta":{"rectStartPointerXY":[3912,1671],"pointRatio":0.5,"geometry":[3912,1671,4446,2089],"type":"BBOX"},"id":"df59a0bb-ffec-4a96-94e7-7af4039fe694","properties":{"create_time":1620527379843,"accept_meta":{},"mark_by":"LABEL","is_system_map":false},"labels":{"标签":"glove"}},{"meta":{"rectStartPointerXY":[3924,1785],"pointRatio":0.5,"geometry":[3924,1785,4137,2323],"type":"BBOX"},"id":"bd4de2d2-fc29-47ba-a7af-f398c790c033","properties":{"create_time":1620527391026,"accept_meta":{},"mark_by":"LABEL","is_system_map":false},"labels":{"标签":"glove"}},{"meta":{"rectStartPointerXY":[3790,433],"pointRatio":0.5,"geometry":[3790,433,4066,1931],"type":"BBOX"},"id":"46cc58e6-1e77-496e-9268-252e8a699d8d","properties":{"create_time":1620527401177,"accept_meta":{},"mark_by":"LABEL","is_system_map":false},"labels":{"标签":"powerchecker"}},{"meta":{"rectStartPointerXY":[3908,1672],"pointRatio":0.5,"geometry":[3919.04,1672,5169,3959],"type":"BBOX"},"id":"2636cdb1-24d0-4651-bf6c-9d773627b3b4","properties":{"create_time":1620527422314,"accept_meta":{},"mark_by":"LABEL","is_system_map":false},"labels":{"标签":"person"}}],"properties":{"seq":"153"},"labels":{"invalid":"false"},"timestamp":1620527439168}
yolo格式
    0 0.5859375 0.6234375 0.1578125 0.14375
    0 0.34375 0.68125 0.1625 0.140625
    0 0.71796875 0.35078125 0.1765625 0.175
'''

import pandas as pd
import json
import os
from PIL import Image, ImageOps


def paddle_xlsx_to_yolo(xlsx_path, images_root, output_dir):
    df = pd.read_excel(xlsx_path,header=None)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for idx, row in df.iterrows():
        print("Processing row:", idx + 1)
        img_excel_path = row.iloc[4]  # 索引从0开始，第5列是4 ,图片excel里面的路径
        img_name = img_excel_path.split('/')[-1]
        img_path = os.path.join(images_root, img_name)  # 图片路径

        label_json_str = row.iloc[5]  # 标签json字符串

        # 打开图片，获取宽高
        with Image.open(img_path) as img:
            img = ImageOps.exif_transpose(img)  # 自动根据 EXIF 方向调整图像
            w, h = img.size
        if (img_name == 'c44ed365_f51d_424c_ae8e_f935834ec9bd.jpg'):
            print(f"width: {w}, height: {h}, image_name: {img_name}")

        label_data = json.loads(label_json_str)
        items = label_data.get('items', [])

        yolo_labels = []
        for item in items:
            label_name = item['labels']['标签']
            if label_name not in class_map:
                continue
            class_id = class_map[label_name]

            geometry = item['meta']['geometry']  # [xmin, ymin, xmax, ymax]
            xmin, ymin, xmax, ymax = geometry

            box_w = xmax - xmin
            box_h = ymax - ymin
            x_center = xmin + box_w / 2
            y_center = ymin + box_h / 2

            x_center_norm = x_center / w
            y_center_norm = y_center / h
            width_norm = box_w / w
            height_norm = box_h / h

            yolo_labels.append(f"{class_id} {x_center_norm:.6f} {y_center_norm:.6f} {width_norm:.6f} {height_norm:.6f}")

        txt_name = os.path.splitext(os.path.basename(img_path))[0] + ".txt"
        txt_path = os.path.join(output_dir, txt_name)

        with open(txt_path, 'w') as f:
            f.write("\n".join(yolo_labels))

    print("转换完成。")


# main
if __name__ == "__main__":
    coco_class_name = ["powerchecker", "glove", "wrongglove", "person", "badge", "operatingbar"] # 替换为你的类别名称
    xlsx_path = r"E:\dataSet\ymj_yolo_data\yolodata\监护袖章、绝缘手套、人、监护袖章、未佩戴绝缘手套、操作杆、验电笔\1train_rname.xlsx"  # 替换为你的xlsx文件路径
    images_root = r"E:\dataSet\ymj_yolo_data\yolodata\监护袖章、绝缘手套、人、监护袖章、未佩戴绝缘手套、操作杆、验电笔\train\images"  # 替换为你的图片根目录
    output_dir = r"E:\dataSet\ymj_yolo_data\yolodata\监护袖章、绝缘手套、人、监护袖章、未佩戴绝缘手套、操作杆、验电笔\train\labels"  # 替换为你希望输出的标签目录

    class_map = {name: idx for idx, name in enumerate(coco_class_name)}
    print("请确认以下路径是否正确：")
    print(f"Excel 文件路径: {xlsx_path}")
    print(f"图片根目录: {images_root}")
    print(f"标签输出目录: {output_dir}")

    confirm = input("确认无误请输入 y，按其他键退出: ").strip().lower()
    if confirm == 'y':
        paddle_xlsx_to_yolo(xlsx_path, images_root, output_dir)
    else:
        print("已取消执行。")