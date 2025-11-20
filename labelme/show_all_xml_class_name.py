"""
展示所有XML文件中的类别名称，统计一共有多少个类别，每个类别的数量

例如 最终返回
class_names = ['car', 'person', 'dog']
total :4
car:1
person:2
dog:1
"""
import os
import xml.etree.ElementTree as ET
from collections import Counter

source_dir = r'E:\work_important\ladder-0909-gs\output_frames2'

class_counter = Counter()

for file in os.listdir(source_dir):
    if file.lower().endswith(".xml"):
        xml_path = os.path.join(source_dir, file)
        tree = ET.parse(xml_path)
        root = tree.getroot()
        for obj in root.findall("object"):
            name = obj.find("name")
            if name is not None:
                class_counter[name.text.strip()] += 1

class_names = list(class_counter.keys())
total = sum(class_counter.values())

print("class_names =", class_names)
print("total:", total)
for cls, count in class_counter.items():
    print(f"{cls}:{count}")
