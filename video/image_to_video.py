import cv2
import os
import glob

def images_to_video(img_dir, out_path="output.mp4", fps=25):
    # 获取所有图片路径
    img_files = sorted(
        glob.glob(os.path.join(img_dir, "*.*")),
        key=lambda x: os.path.basename(x)
    )

    if not img_files:
        print("❌ 没有找到图片")
        return

    # 读取第一张图获取尺寸
    first_img = cv2.imread(img_files[0])
    if first_img is None:
        print("❌ 读取第一张图片失败")
        return

    h, w = first_img.shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # 保存为 mp4 格式
    video = cv2.VideoWriter(out_path, fourcc, fps, (w, h))

    for i, img_path in enumerate(img_files):
        img = cv2.imread(img_path)
        if img is None:
            print(f"⚠️ 跳过坏图: {img_path}")
            continue

        # 如果大小不一致，强制缩放
        if img.shape[:2] != (h, w):
            img = cv2.resize(img, (w, h))

        video.write(img)
        print(f"写入第 {i+1}/{len(img_files)} 帧: {img_path}")

    video.release()
    print(f"✅ 视频已保存到 {out_path}")


if __name__ == "__main__":
    img_dir = r"E:\myJobTwo\project\train-helper\paddle\ocr\server_TextDetection_output"   # 修改为图片文件夹路径
    out_path = "output.mp4"
    images_to_video(img_dir, out_path, fps=5)
