import os
import xml.etree.ElementTree as ET

ANNOTATIONS_DIR = "z_datasets_test/images"  # Thư mục chứa các file XML
OUTPUT_FILE = "z_datasets_test/annotations/label_map.pbtxt"  # Tên file output

def extract_labels(annotations_dir):
    labels = set()
    for filename in os.listdir(annotations_dir):
        if not filename.endswith('.xml'):
            continue
        tree = ET.parse(os.path.join(annotations_dir, filename))
        root = tree.getroot()
        for obj in root.findall('object'):
            name = obj.find('name').text.strip()
            labels.add(name)
    return sorted(labels)

def create_label_map(labels, output_file):
    with open(output_file, 'w') as f:
        for idx, label in enumerate(labels, start=1):
            f.write("item {\n")
            f.write(f"    id: {idx}\n")
            f.write(f"    name: '{label}'\n")
            f.write("}\n\n")
    print(f"✅ Created {output_file} with {len(labels)} labels.")

if __name__ == "__main__":
    labels = extract_labels(ANNOTATIONS_DIR)
    create_label_map(labels, OUTPUT_FILE)
