"""
遍历 YAML 里的所有 train/val 数据路径，逐个检查图片和标签是否能正常读取，避免训练时因为路径错、图片损坏、标签缺失出错。
"""

import os
import cv2
import yaml

def check_dataset(yaml_path):
    with open(yaml_path, "r", encoding="utf-8") as f:
        data_cfg = yaml.safe_load(f)

    all_sets = {"train": data_cfg["train"], "val": data_cfg["val"]}
    exts = [".jpg", ".jpeg", ".png"]

    for split, dirs in all_sets.items():
        print(f"\n🔍 Checking {split} set...")
        for d in dirs:
            img_dir = os.path.abspath(d)
            label_dir = img_dir.replace("images", "labels")
            if not os.path.exists(img_dir):
                print(f"❌ Missing image dir: {img_dir}")
                continue
            if not os.path.exists(label_dir):
                print(f"⚠️ Missing label dir: {label_dir}")
                continue

            img_files = [f for f in os.listdir(img_dir) if os.path.splitext(f)[1].lower() in exts]
            for img_file in img_files:
                img_path = os.path.join(img_dir, img_file)
                label_path = os.path.join(label_dir, os.path.splitext(img_file)[0] + ".txt")

                # 1. 检查图片能否读取
                im = cv2.imread(img_path)
                if im is None:
                    print(f"❌ Bad image: {img_path}")
                    continue

                # 2. 检查标签是否存在
                if not os.path.exists(label_path):
                    print(f"⚠️ Missing label: {label_path}")
                    continue

                # 3. 检查标签内容
                with open(label_path, "r") as lf:
                    for i, line in enumerate(lf, 1):
                        parts = line.strip().split()
                        if len(parts) == 0:
                            continue
                        if len(parts) != 5:
                            print(f"⚠️ Bad label format {label_path}:{i} -> {line.strip()}")
                            continue
                        try:
                            cls, x, y, w, h = map(float, parts)
                            assert 0 <= x <= 1 and 0 <= y <= 1 and 0 <= w <= 1 and 0 <= h <= 1
                        except Exception as e:
                            print(f"❌ Invalid label value {label_path}:{i} -> {line.strip()} ({e})")

    print("\n✅ Dataset check finished.")


if __name__ == "__main__":
    check_dataset(r"haitu_5.yaml")
