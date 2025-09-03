import cv2
import numpy as np
import os

def letterbox(im, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True, stride=32):
    """Resizes and pads image to new_shape with stride-multiple constraints, returns resized image, ratio, padding."""
    shape = im.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better val mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return im, ratio, (dw, dh)


def load_labels(label_path):
    """读取标签文件，并转换成浮点数列表"""
    labels = []
    with open(label_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            label = list(map(float, line.strip().split()))
            labels.append(label)
    return labels

def resize_labels(labels, ratio, pad, img_shape,new_size):
    """根据缩放比例和填充值调整标签坐标"""
    new_labels = []
    for label in labels:
        if len(label) == 0 :
            continue
        # 将归一化坐标转换为实际像素坐标
        x_center = label[1] * img_shape[1]
        y_center = label[2] * img_shape[0]
        width = label[3] * img_shape[1]
        height = label[4] * img_shape[0]

        # 根据缩放比例调整坐标
        x_center = x_center * ratio[0] + pad[0]
        y_center = y_center * ratio[1] + pad[1]
        width = width * ratio[0]
        height = height * ratio[1]

        # 将实际像素坐标转换回归一化坐标
        x_center /= new_size[0]
        y_center /= new_size[1]
        width /= new_size[0]
        height /= new_size[1]

        # 确保坐标在 [0, 1] 范围内
        x_center = max(0, min(1, x_center))
        y_center = max(0, min(1, y_center))
        width = max(0, min(1, width))
        height = max(0, min(1, height))

        # 将调整后的标签添加到新标签列表中
        new_labels.append([int(label[0]), x_center, y_center, width, height])

    return new_labels

def resize_images_and_labels(image_dir, label_dir, output_image_dir, output_label_dir, new_size=(640, 640)):
    # Create output directories if they do not exist
    os.makedirs(output_image_dir, exist_ok=True)
    os.makedirs(output_label_dir, exist_ok=True)

    # Iterate over all images in the image directory
    idx = 1
    for image_name in os.listdir(image_dir):
        idx += 1
        print(f"Processing image {idx}: {image_name}")
        if image_name.endswith(('.jpg', '.png', '.jpeg','.JPG', '.PNG', '.JPEG')):
            image_path = os.path.join(image_dir, image_name)
            label_path = os.path.join(label_dir, image_name.replace(image_name.split('.')[-1], 'txt'))

            # Read image
            img = cv2.imread(image_path)
            labels = load_labels(label_path)


            # Resize image and labels
            resized_img, ratio, pad = letterbox(img, new_shape=new_size,auto=False)
            new_labels = resize_labels(labels, ratio, pad, img.shape,new_size)

            # Save resized image
            cv2.imwrite(os.path.join(output_image_dir, image_name), resized_img)

            # Save resized labels
            with open(os.path.join(output_label_dir, image_name.replace(image_name.split('.')[-1], 'txt')), 'w') as f:
                for label in new_labels:
                    f.write(' '.join(map(str, label)) + '\n')




# 注意 ！！！
# 注意 ！！！
# 注意 ！！！
# 1. 不要直接使用yolo detect的图片，那个图标被自动打上标记了！！！
image_dir = r'E:\dataSet\ymj_yolo_data\yolodata\helmet-reflectiveJacket\train\images'
# 1. 不要直接使用yolo detect的图片，那个图标被自动打上标记了！！！
# 注意 ！！！
# 注意 ！！！
# 注意 ！！！
label_dir = r'E:\dataSet\ymj_yolo_data\yolodata\helmet-reflectiveJacket\train\labels_class_5'


output_image_dir = r'E:\dataSet\ymj_yolo_data\yolodata\helmet-reflectiveJacket\train\images-640-class-5\images'
output_label_dir = r'E:\dataSet\ymj_yolo_data\yolodata\helmet-reflectiveJacket\train\images-640-class-5\labels'

resize_images_and_labels(image_dir, label_dir, output_image_dir, output_label_dir, new_size=(640, 640))
