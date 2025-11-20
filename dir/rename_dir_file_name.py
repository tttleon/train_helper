import os

# 目标目录
folder = r"E:\work_important\钢包现场视频\泉州闽光\100-32t\右耳轴"

# 获取目录下所有文件（排除子目录），并按名称排序
files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
files.sort()

# 依次重命名
for i, filename in enumerate(files, start=1):
    # 获取文件扩展名
    ext = os.path.splitext(filename)[1]
    # 新文件名，例如 1.mp4
    new_name = f"{i}{ext}"
    # 旧文件路径
    old_path = os.path.join(folder, filename)
    # 新文件路径
    new_path = os.path.join(folder, new_name)
    os.rename(old_path, new_path)

print("重命名完成。")
