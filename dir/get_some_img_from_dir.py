import os
import random
import shutil

def get_all_image_files(source_dir, image_extensions):
    """
    递归获取指定目录下所有图片文件的路径。

    Args:
        source_dir (str): 源目录路径。
        image_extensions (tuple): 支持的图片文件扩展名元组。

    Returns:
        list: 所有图片文件的完整路径列表。
    """
    image_files = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(image_extensions):
                image_files.append(os.path.join(root, file))
    return image_files

def copy_random_images(source_dir, dest_dir, num_images, image_extensions=('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
    """
    从源目录中随机抽取指定数量的【不重复】图片并复制到目标目录。

    Args:
        source_dir (str): 源目录路径。
        dest_dir (str): 目标目录路径。
        num_images (int): 需要抽取的图片数量。
        image_extensions (tuple, optional): 支持的图片文件扩展名。
                                            Defaults to ('.jpg', '.jpeg', '.png', '.gif', '.bmp').
    """
    # 确保目标目录存在
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # 1. 获取所有不重复的图片文件路径
    all_images = get_all_image_files(source_dir, image_extensions)

    if not all_images:
        print("在源目录中没有找到任何图片。")
        return

    # 2. 确定实际要抽取的图片数量
    # 如果请求的数量大于图片总数，则只抽取所有图片
    num_to_copy = min(num_images, len(all_images))
    if num_to_copy < num_images:
        print(f"警告: 源目录中的图片总数 ({len(all_images)}) 少于要求抽取的数量 ({num_images})。")
        print(f"将复制所有找到的 {len(all_images)} 张图片。")

    # 3. 【核心步骤】进行无重复的随机抽样
    # random.sample() 函数会从 all_images 列表中随机选取 num_to_copy 个【唯一的】元素。
    # 它保证了返回的列表中不会有任何重复项。
    random_images = random.sample(all_images, num_to_copy)

    # 4. 复制抽样后的图片到目标目录
    copied_count = 0
    print(f"正在复制 {len(random_images)} 张不重复的图片...")
    for image_path in random_images:
        try:
            # 使用 copy2 保留文件的元数据（如创建时间）
            new_random_name = f"{copied_count+1:03d}" + os.path.splitext(image_path)[1]
            dest_path = os.path.join(dest_dir, new_random_name)
            shutil.copy2(image_path, dest_path)
            copied_count += 1
        except Exception as e:
            print(f"复制文件 {image_path} 时出错: {e}")

    print(f"操作完成！成功复制 {copied_count} 张不重复的图片到 '{dest_dir}' 目录。")

if __name__ == '__main__':
    # --- 用户配置区域 ---

    # 1. 源图片目录 (请替换为你的实际路径)
    # Windows 示例: "C:\\Users\\YourUser\\Pictures"
    # macOS/Linux 示例: "/home/user/pictures"
    SOURCE_DIRECTORY = r"E:\work_important\中冶钢铁\20250509"  # 修改为你的源目录

    # 2. 目标目录 (请替换为你的实际路径)
    # Windows 示例: "C:\\Users\\YourUser\\Desktop\\Random_Pics"
    # macOS/Linux 示例: "/home/user/random_pics"
    DESTINATION_DIRECTORY = r"E:\dockerImage\pulsar2\data\nafnet\calibration_dataset"  # 修改为你的目标目录

    # 3. 想要抽取的图片数量
    NUMBER_OF_IMAGES_TO_COPY = 32

    # 4. (可选) 支持的图片格式
    IMAGE_FORMATS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')

    # --- 执行脚本 ---
    copy_random_images(SOURCE_DIRECTORY, DESTINATION_DIRECTORY, NUMBER_OF_IMAGES_TO_COPY, IMAGE_FORMATS)