import cv2
import numpy as np
import os
import json
from pathlib import Path


def rotate_image_and_points(img, polys, angle):
    """
    逆时针旋转图像和多边形点。
    angle: 0/90/180/270 逆时针角度
    polys: list of np.array 4x2
    """
    H, W = img.shape[:2]
    if angle == 0:
        return img, polys
    elif angle == 90:
        # 逆时针旋转 90 度
        rotated = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        new_polys = [np.array([[y, W - x] for x, y in poly], dtype=int) for poly in polys]
    elif angle == 180:
        # 逆时针旋转 180 度
        rotated = cv2.rotate(img, cv2.ROTATE_180)
        new_polys = [np.array([[W - x, H - y] for x, y in poly], dtype=int) for poly in polys]
    elif angle == 270:
        # 逆时针旋转 270 度，等同于顺时针旋转 90 度
        rotated = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        new_polys = [np.array([[H - y, x] for x, y in poly], dtype=int) for poly in polys]
    else:
        raise ValueError("只支持 0/90/180/270 逆时针旋转")
    return rotated, new_polys


def determine_rotation(polys):
    """
    根据四边形几何判断旋转角度。
    OCR结果应为两行，上长下短，且左对齐（透视效果）。
    此函数会检测四种可能的旋转角度（0, 90, 180, 270度）。

    参数：
    polys (list): 包含两个或更多四边形坐标的列表。每个四边形是 np.array([[x1, y1], [x2, y2], ...])。

    返回：
    int: 旋转角度 (0, 90, 180, 270)。
    """
    # 计算两个四边形的面积
    if len(polys) < 2:
        print('少于两个四边形，无法判断，默认不旋转，经检查默认返回0角度')
        return 0
    area_one = cv2.contourArea(polys[0])
    area_two = cv2.contourArea(polys[1])

    # 面积大的是四个数字的，面积小的是两个数字的
    if area_one > area_two:
        four_num_det = polys[0]
        two_num_det =  polys[1]
    elif area_one < area_two:
        four_num_det = polys[1]
        two_num_det =  polys[0]
    else:
        print('两个四边形面积相等，无法判断，默认不旋转，经检查默认返回0角度')
        return 0

    # 判断四个数字的矩形框是水平还是垂直，利用x最大最小差值 和 y最大最小差值进行对比
    x_coords = four_num_det[:, 0]
    y_coords = four_num_det[:, 1]
    x_range = x_coords.max() - x_coords.min()
    y_range = y_coords.max() - y_coords.min()

    four_num_top_left = four_num_det[np.argmin(four_num_det[:, 0] + four_num_det[:, 1])]
    two_num_top_left = two_num_det[np.argmin(two_num_det[:, 0] + two_num_det[:, 1])]
    if x_range >= y_range:
        # 水平方向的，那么判断是0度还是180度
        # 四个数字的正常情况下是在上面
        # 判断两个四边形的左上角点，如果四个数字的左上角点的y值小于两个数字的左上角点的y值，说明是0度，否则是180度
        if four_num_top_left[1] < two_num_top_left[1]:
            return 0
        else:
            return 180
    else:
        # 垂直方向的，那么判断是90度还是270度
        # 判断两个四边形的左上角点，如果四个数字的左上角点的x值小于两个数字的左上角点的x值，说明是270度，否则90度
        if four_num_top_left[0] < two_num_top_left[0]:
            return 270
        else:
            return 90






def process_from_label(txt_file, save_dir, output_txt, crop_size=640):
    os.makedirs(save_dir, exist_ok=True)
    out_lines = []
    file_state_out_lines = []

    with open(txt_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            img_path, json_str = line.split("\t", 1)
            annotations = json.loads(json_str)
        except Exception as e:
            print(f"解析错误: {line} ({e})")
            continue

        polys = [np.array(anno["points"], dtype=int) for anno in annotations]
        if not polys:
            continue

        # 拼接路径text_file_dir
        if not os.path.isabs(img_path):
            img_path = os.path.join(text_file_dir, img_path)
        img = cv2.imread(img_path)
        if img is None:
            continue

        # 裁剪中心：所有点的外接矩形中心
        all_points = np.vstack(polys)
        x, y, w, h = cv2.boundingRect(all_points)
        cx, cy = x + w // 2, y + h // 2

        H, W = img.shape[:2]
        half = crop_size // 2
        x1 = max(0, cx - half)
        y1 = max(0, cy - half)
        x2 = min(W, cx + half)
        y2 = min(H, cy + half)

        crop = img[y1:y2, x1:x2]

        # 坐标映射到 crop 内
        polys_shifted = [poly - [x1, y1] for poly in polys]

        # padding
        if crop.shape[0] != crop_size or crop.shape[1] != crop_size:
            padded = np.zeros((crop_size, crop_size, 3), dtype=np.uint8)
            padded[:crop.shape[0], :crop.shape[1]] = crop
            crop = padded

        # 判断旋转角度
        angle = determine_rotation(polys_shifted)
        print(f'img_path={img_path}, angle={angle}')

        # 旋转图像和坐标
        crop_rotated, polys_oriented = rotate_image_and_points(crop, polys_shifted, angle)

        # 保存裁剪后的图
        filename = os.path.basename(img_path)
        # save_path = os.path.join(save_dir, filename)
        save_path = save_dir + '/' + filename
        cv2.imwrite(save_path, crop_rotated)

        # 写新的标注
        new_annos = []
        for anno, poly in zip(annotations, polys_oriented):
            new_annos.append({
                "transcription": anno["transcription"],
                "points": [[int(x), int(y)] for x, y in poly],
                "difficult": bool(anno.get("difficult", False))
            })
        out_line = f"{save_path}\t{json.dumps(new_annos, ensure_ascii=False)}"
        out_lines.append(out_line)
        file_state_out_line = f'{save_path}	1'
        file_state_out_lines.append(file_state_out_line)

    with open(output_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))
    with open("fileState.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(file_state_out_lines))


if __name__ == "__main__":
    text_file_dir = f'E:\dataSet\ocr\mcc_icon'
    txt_file = r"E:\dataSet\ocr\mcc_icon\paddle_label\Label.txt"
    save_dir = "paddle_label_crop_oriented"
    output_txt = "Label.txt"
    process_from_label(txt_file, save_dir, output_txt, crop_size=640)
