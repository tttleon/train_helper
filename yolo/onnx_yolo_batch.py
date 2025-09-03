import hashlib
from pathlib import Path

import cv2
import numpy as np
import onnxruntime as ort
import time


# 初始化ONNX Runtime的GPU会话
def create_onnx_session(model_path):
    providers = [
        ('CUDAExecutionProvider', {
            'device_id': 0,
            'arena_extend_strategy': 'kNextPowerOfTwo',
            'gpu_mem_limit': 2 * 1024 * 1024 * 1024,  # 2GB
            'cudnn_conv_algo_search': 'EXHAUSTIVE',
            'do_copy_in_default_stream': True,
        }),
        'CPUExecutionProvider'
    ]
    session = ort.InferenceSession(model_path, providers=providers)
    return session


# 预处理函数
def preprocess(img, input_size=(640, 640)):
    h, w = img.shape[:2]
    scale = min(input_size[0] / h, input_size[1] / w)
    nh, nw = int(h * scale), int(w * scale)
    top = (input_size[0] - nh) // 2
    left = (input_size[1] - nw) // 2

    # 缩放
    resized = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LINEAR)
    canvas = np.full((input_size[0], input_size[1], 3), 114, dtype=np.uint8)
    canvas[top:top+nh, left:left+nw] = resized

    # 转换格式
    canvas = canvas.astype(np.float32) / 255.0
    canvas = np.transpose(canvas, (2, 0, 1))
    canvas = np.expand_dims(canvas, axis=0)

    return canvas, (w, h), scale, top, left  # 👈 加了 top 和 left


# 后处理函数 - 非极大值抑制
def nms(boxes, scores, iou_threshold=0.45):
    # 按置信度排序
    order = scores.argsort()[::-1]
    keep = []

    while order.size > 0:
        i = order[0]
        keep.append(i)

        # 计算IOU
        xx1 = np.maximum(boxes[i, 0], boxes[order[1:], 0])
        yy1 = np.maximum(boxes[i, 1], boxes[order[1:], 1])
        xx2 = np.minimum(boxes[i, 2], boxes[order[1:], 2])
        yy2 = np.minimum(boxes[i, 3], boxes[order[1:], 3])

        w = np.maximum(0.0, xx2 - xx1)
        h = np.maximum(0.0, yy2 - yy1)
        intersection = w * h

        area1 = (boxes[i, 2] - boxes[i, 0]) * (boxes[i, 3] - boxes[i, 1])
        area2 = (boxes[order[1:], 2] - boxes[order[1:], 0]) * (boxes[order[1:], 3] - boxes[order[1:], 1])
        union = area1 + area2 - intersection

        iou = intersection / union

        # 保留IOU小于阈值的框
        inds = np.where(iou <= iou_threshold)[0]
        order = order[inds + 1]

    return keep


# 后处理函数
def postprocess(output, orig_shape, scale, top, left, conf_threshold=0.7, iou_threshold=0.45):
    boxes = output[:, :4]
    conf = output[:, 4:5]
    cls_scores = output[:, 5:]

    scores = conf * cls_scores
    class_ids = np.argmax(scores, axis=1)
    max_scores = np.max(scores, axis=1)

    mask = max_scores > conf_threshold
    boxes = boxes[mask]
    scores = max_scores[mask]
    class_ids = class_ids[mask]

    if len(boxes) == 0:
        return [], [], []

    # 转换为 xyxy
    boxes[:, 0] = boxes[:, 0] - boxes[:, 2] / 2
    boxes[:, 1] = boxes[:, 1] - boxes[:, 3] / 2
    boxes[:, 2] = boxes[:, 0] + boxes[:, 2]
    boxes[:, 3] = boxes[:, 1] + boxes[:, 3]

    # 👇 修复坐标偏移：减去填充，再除以缩放
    boxes[:, [0, 2]] -= left
    boxes[:, [1, 3]] -= top
    boxes /= scale

    boxes[:, [0, 2]] = np.clip(boxes[:, [0, 2]], 0, orig_shape[0])
    boxes[:, [1, 3]] = np.clip(boxes[:, [1, 3]], 0, orig_shape[1])

    keep = nms(boxes, scores, iou_threshold)
    return boxes[keep], scores[keep], class_ids[keep]


# 绘制结果
def draw_detections(img, boxes, scores, class_ids, class_names):
    color_map = {
        0: (0, 255, 0),  # 绿色
        1: (255, 0, 0),  # 蓝色
        2: (0, 0, 255),  # 红色
        3: (255, 255, 0),  # 青色
        4: (255, 0, 255),  # 品红
        5: (0, 255, 255),  # 黄色
        6: (128, 0, 128),  # 紫色
        7: (128, 128, 0),  # 橄榄色
        8: (0, 128, 128),  # 青绿色
        9: (128, 128, 128)  # 灰色
    }

    for box, score, class_id in zip(boxes, scores, class_ids):
        x1, y1, x2, y2 = map(int, box)
        color = color_map[class_id]

        # 画框
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 10)

        # 显示标签和置信度
        label = f"{class_names[class_id]}: {score:.2f}"
        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 5, color, 2)

    return img

def process_images_in_directory(session, input_dir, output_dir, class_names, preserve_structure=False):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']

    for img_path in input_dir.rglob("*"):
        if img_path.suffix.lower() not in image_extensions:
            continue

        # 读取图片
        img = cv2.imread(str(img_path))
        if img is None:
            print(f"Failed to read image: {img_path}")
            continue

        input_tensor, orig_shape, scale, top, left = preprocess(img)
        outputs = session.run(None, {session.get_inputs()[0].name: input_tensor})
        output = outputs[0][0]

        boxes, scores, class_ids = postprocess(output, orig_shape, scale, top, left)

        # 生成唯一ID用于重命名，避免重复
        img_hash = hashlib.md5(str(img_path).encode()).hexdigest()[:8]

        for i, (box, score, class_id) in enumerate(zip(boxes, scores, class_ids)):
            x1, y1, x2, y2 = map(int, box)
            cropped = img[y1:y2, x1:x2]

            if preserve_structure:
                save_dir = output_dir / class_names[class_id] / img_path.parent.relative_to(input_dir)
            else:
                save_dir = output_dir / class_names[class_id]

            save_dir.mkdir(parents=True, exist_ok=True)

            crop_filename = save_dir / f"{img_path.stem}_{img_hash}_det{i}_score{score:.2f}.jpg"
            cv2.imwrite(str(crop_filename), cropped)

        # === 保存带框图像 ===
        img_with_boxes = draw_detections(img.copy(), boxes, scores, class_ids, class_names)

        if preserve_structure:
            result_img_path = output_dir / "annotated" / img_path.relative_to(input_dir)
        else:
            result_img_path = output_dir / "annotated" / f"{img_path.stem}_{img_hash}.jpg"

        result_img_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(result_img_path), img_with_boxes)

        print(f"Processed: {img_path} -> {result_img_path}")

# 主函数
# === 主函数 ===
def main():
    model_path = r"E:\myJobTwo\project\yolov5-master\data\haitu-ningxia\exp_a\weights\best-no-fall-op12.onnx"
    input_dir = r"E:\work_important\haiotu-yolo\20250815"  # 替换为你存放图片的目录
    output_dir = "output"  # 检测结果输出目录
    class_names = ['person','hat','head','reflectiveJacket',"hand","ladder",'glove','fall']  # 替换为你的类别名称列表


    session = create_onnx_session(model_path)
    process_images_in_directory(session, input_dir, output_dir, class_names)


if __name__ == "__main__":
    main()