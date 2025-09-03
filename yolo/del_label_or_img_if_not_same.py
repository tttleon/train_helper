import os
import argparse

def get_name_without_ext_set(directory):
    """获取不带扩展名的文件名集合和映射"""
    name_set = set()
    file_map = {}
    for file in os.listdir(directory):
        full_path = os.path.join(directory, file)
        if os.path.isfile(full_path):
            name, _ = os.path.splitext(file)
            name_set.add(name)
            file_map[name] = full_path
    return name_set, file_map

def sync_dirs_ignore_ext(dir_a, dir_b):
    names_a, map_a = get_name_without_ext_set(dir_a)
    names_b, map_b = get_name_without_ext_set(dir_b)

    only_in_a = names_a - names_b
    only_in_b = names_b - names_a

    for name in only_in_a:
        print(f"Deleting from A: {map_a[name]}")
        os.remove(map_a[name])

    for name in only_in_b:
        print(f"Deleting from B: {map_b[name]}")
        os.remove(map_b[name])

    print("Synchronization complete. Files match by name (ignoring extension).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync files by name only (ignore extensions).")
    parser.add_argument("dir_a", help="Path to directory A")
    parser.add_argument("dir_b", help="Path to directory B")

    dir_a = r'E:\dataSet\ymj_u2net_data\blue_mask-del\gt_aug'
    dir_b = r'E:\dataSet\ymj_u2net_data\blue_mask-del\im_aug'
    sync_dirs_ignore_ext(dir_a,dir_b)
