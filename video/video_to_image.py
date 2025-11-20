'''
把视频转换为图片保存
'''

import cv2
import os


def video_to_images(video_path, output_dir, frame_interval=30):
    # 创建输出文件夹
    os.makedirs(output_dir, exist_ok=True)

    # 打开视频
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("无法打开视频文件")
        return

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # 视频结束

        if frame_count % frame_interval == 0:
            image_path = os.path.join(output_dir, f"32-frame_{frame_count:06d}.jpg")
            cv2.imwrite(image_path, frame)
            saved_count += 1

        frame_count += 1

    cap.release()
    print(f"总共提取并保存了 {saved_count} 张图片。")


# 示例用法
video_to_images(r"E:\视频制作\剪辑过的素材\00000001570000000.mp4_no_audio.mp4", "./output_images", frame_interval=10)
