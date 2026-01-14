import os
import re


def remove_chinese_from_filenames(directory_path):
    """
    删除指定目录下所有图片文件名中的中文字符
    """
    # 支持的图片扩展名
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']

    # 匹配中文字符的正则表达式
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')

    try:
        # 遍历目录下的所有文件
        for filename in os.listdir(directory_path):
            # 获取文件完整路径
            file_path = os.path.join(directory_path, filename)

            # 只处理文件，不处理文件夹
            if os.path.isfile(file_path):
                # 检查文件扩展名是否是图片
                file_ext = os.path.splitext(filename)[1].lower()
                if file_ext in image_extensions:
                    # 分离文件名和扩展名
                    name_without_ext, extension = os.path.splitext(filename)

                    # 删除文件名中的中文字符（保留扩展名前的部分）
                    new_name_without_ext = chinese_pattern.sub('', name_without_ext)

                    # 如果删除中文后文件名不为空，则重命名
                    if new_name_without_ext != name_without_ext:
                        # 构建新文件名
                        new_filename = new_name_without_ext + extension
                        new_file_path = os.path.join(directory_path, new_filename)

                        # 处理文件名冲突
                        counter = 1
                        while os.path.exists(new_file_path):
                            new_filename = f"{new_name_without_ext}_{counter}{extension}"
                            new_file_path = os.path.join(directory_path, new_filename)
                            counter += 1

                        # 重命名文件
                        os.rename(file_path, new_file_path)
                        print(f"重命名: {filename} -> {new_filename}")

        print("处理完成！")

    except Exception as e:
        print(f"处理过程中出现错误: {e}")


# 使用示例
if __name__ == "__main__":
    # 设置你的目录路径
    directory = r"E:\work_important\TC试剂\test_img#251201\xiaomi"

    # 确认用户是否要继续
    print(f"将要处理的目录: {directory}")
    print("这个脚本会重命名该目录下的所有图片文件，删除文件名中的中文字符。")
    confirm = input("确认要继续吗？(输入 'yes' 继续): ")

    if confirm.lower() == 'yes':
        remove_chinese_from_filenames(directory)
    else:
        print("操作已取消。")