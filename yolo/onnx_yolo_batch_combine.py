import hashlib
from pathlib import Path
import cv2
import numpy as np
import onnxruntime as ort


# 初始化ONNX Runtime的GPU会话
def create_onnx_session(model_path):
    providers = [
        ('CUDAExecutionProvider', {
            'device_id': 0,
            'arena_extend_strategy': 'kNextPowerOfTwo',
            'gpu_mem_limit': 2 * 1024 * 1024 * 1024,
            'cudnn_conv_algo_search': 'EXHAUSTIVE',
            'do_copy_in_default_stream': True,
        }),
        'CPUExecutionProvider'
    ]
    return ort.InferenceSession(model_path, providers=providers)


# 输入预处理
def preprocess(img, input_size=(640, 640)):
    h, w = img.shape[:2]
    scale = min(input_size[0] / h, input_size[1] / w)
    nh, nw = int(h * scale), int(w * scale)
    top = (input_size[0] - nh) // 2
    left = (input_size[1] - nw) // 2

    resized = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LINEAR)
    canvas = np.full((input_size[0], input_size[1], 3), 114, dtype=np.uint8)
    canvas[top:top + nh, left:left + nw] = resized

    canvas = canvas.astype(np.float32) / 255.0
    canvas = np.transpose(canvas, (2, 0, 1))
    canvas = np.expand_dims(canvas, axis=0)

    return canvas, (w, h), scale, top, left


# 非极大值抑制
def nms(boxes, scores, iou_threshold=0.45):
    order = scores.argsort()[::-1]
    keep = []

    while order.size > 0:
        i = order[0]
        keep.append(i)

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

        inds = np.where(iou <= iou_threshold)[0]
        order = order[inds + 1]

    return keep


# 后处理
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

    boxes[:, 0] = boxes[:, 0] - boxes[:, 2] / 2
    boxes[:, 1] = boxes[:, 1] - boxes[:, 3] / 2
    boxes[:, 2] = boxes[:, 0] + boxes[:, 2]
    boxes[:, 3] = boxes[:, 1] + boxes[:, 3]

    boxes[:, [0, 2]] -= left
    boxes[:, [1, 3]] -= top
    boxes /= scale

    boxes[:, [0, 2]] = np.clip(boxes[:, [0, 2]], 0, orig_shape[0])
    boxes[:, [1, 3]] = np.clip(boxes[:, [1, 3]], 0, orig_shape[1])

    keep = nms(boxes, scores, iou_threshold)
    return boxes[keep], scores[keep], class_ids[keep]


# 将多个head的输出 reshape 并拼接成统一的 [N, no]
def decode_outputs(outputs):
    all = [o.reshape(-1, o.shape[-1]) for o in outputs]
    return np.concatenate(all, axis=0)  # shape: [N, no]


# 绘图
def draw_detections(img, boxes, scores, class_ids, class_names):
    color_map = {
        0: (0, 255, 0), 1: (255, 0, 0), 2: (0, 0, 255),
        3: (255, 255, 0), 4: (255, 0, 255), 5: (0, 255, 255),
        6: (128, 0, 128), 7: (128, 128, 0), 8: (0, 128, 128),
        9: (128, 128, 128)
    }

    for box, score, class_id in zip(boxes, scores, class_ids):
        x1, y1, x2, y2 = map(int, box)
        color = color_map.get(class_id % 10, (255, 255, 255))
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        label = f"{class_names[class_id]}: {score:.2f}"
        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    return img


# 主流程
def process_images_in_directory(session, input_dir, output_dir, class_names, preserve_structure=False):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']

    for img_path in input_dir.rglob("*"):
        if img_path.suffix.lower() not in image_extensions:
            continue

        img = cv2.imread(str(img_path))
        if img is None:
            print(f"Failed to read image: {img_path}")
            continue

        input_tensor, orig_shape, scale, top, left = preprocess(img)
        outputs = session.run(None, {session.get_inputs()[0].name: input_tensor})
        output = decode_outputs(outputs)

        boxes, scores, class_ids = postprocess(output, orig_shape, scale, top, left)

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

        img_with_boxes = draw_detections(img.copy(), boxes, scores, class_ids, class_names)
        if preserve_structure:
            result_img_path = output_dir / "annotated" / img_path.relative_to(input_dir)
        else:
            result_img_path = output_dir / "annotated" / f"{img_path.stem}_{img_hash}.jpg"
        result_img_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(result_img_path), img_with_boxes)
        print(f"Processed: {img_path} -> {result_img_path}")


# 主函数入口
def main():
    model_path = "./onnx_model/combine/person_hat_head_reflectiveJacket_layer14_combine.onnx"
    input_dir = r"./input"
    output_dir = "./output"
    class_names = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']  # 替换为你的类别名称
    session = create_onnx_session(model_path)
    process_images_in_directory(session, input_dir, output_dir, class_names)


if __name__ == "__main__":
    main()
