import os
import cv2
import glob
from lxml import etree
from lxml.builder import E

# ⚙️ Cấu hình
IMG_DIR = 'z_datasets_test/images'
LABEL_DIR = 'z_datasets_test/labels'
OUT_ANNOTATION_DIR = 'z_datasets_test/annotations/xmls'
CLASSES = [
    'MMs_peanut'
    ,'MMs_regular'
    ,'airheads'
    ,'gummy_worms'
    ,'milky_way'
    ,'nerds'
    ,'skittles'
    ,'snickers'
    ,'starbust'
    ,'three_musketeers'
    ,'twizzlers'
] 

os.makedirs(OUT_ANNOTATION_DIR, exist_ok=True)

def convert_annotation(img_path, label_path, output_path):
    filename = os.path.basename(img_path)
    image = cv2.imread(img_path)
    h, w, _ = image.shape

    annotation = E.annotation(
        E.folder(os.path.basename(os.path.dirname(img_path))),
        E.filename(filename),
        E.path(os.path.abspath(img_path)),
        E.source(E.database("Unknown")),
        E.size(E.width(str(w)), E.height(str(h)), E.depth("3")),
        E.segmented("0")
    )

    with open(label_path, 'r') as f:
        for line in f.readlines():
            parts = line.strip().split()
            class_id = int(parts[0])
            x_center, y_center, box_w, box_h = map(float, parts[1:])
            xmin = int((x_center - box_w / 2) * w)
            xmax = int((x_center + box_w / 2) * w)
            ymin = int((y_center - box_h / 2) * h)
            ymax = int((y_center + box_h / 2) * h)

            object_ = E.object(
                E.name(CLASSES[class_id]),
                E.pose("Unspecified"),
                E.truncated("0"),
                E.difficult("0"),
                E.bndbox(
                    E.xmin(str(max(0, xmin))),
                    E.ymin(str(max(0, ymin))),
                    E.xmax(str(min(w, xmax))),
                    E.ymax(str(min(h, ymax)))
                )
            )
            annotation.append(object_)

    tree = etree.ElementTree(annotation)
    tree.write(output_path, pretty_print=True)

# 🔁 Lặp qua tất cả file txt
label_files = glob.glob(os.path.join(LABEL_DIR, "*.txt"))
for label_file in label_files:
    img_file = os.path.join(IMG_DIR, os.path.splitext(os.path.basename(label_file))[0] + ".jpg")
    if os.path.exists(img_file):
        xml_out = os.path.join(OUT_ANNOTATION_DIR, os.path.splitext(os.path.basename(label_file))[0] + ".xml")
        convert_annotation(img_file, label_file, xml_out)
