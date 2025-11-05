import os
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
import csv

# Rutas
DATASET_ORIG = Path('cows-detection-dataset')
IMAGES_ORIG = DATASET_ORIG / 'images'
ANNOTATIONS = DATASET_ORIG / 'annotations.xml'
CSV_FILE = DATASET_ORIG / 'cows.csv'

DATASET_OUT = Path('dataset')
IMAGES_OUT = DATASET_OUT / 'images'
LABELS_OUT = DATASET_OUT / 'labels'
IMAGES_OUT.mkdir(parents=True, exist_ok=True)
LABELS_OUT.mkdir(parents=True, exist_ok=True)

# Leer lista de imágenes válidas desde cows.csv
valid_images = set()
with open(CSV_FILE, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        img_name = row['image_name'].split('/')[-1]
        valid_images.add(img_name)

# Parsear XML
tree = ET.parse(ANNOTATIONS)
root = tree.getroot()

for image in root.findall('image'):
    img_name = image.get('name').split('/')[-1]
    if img_name not in valid_images:
        continue
    width = float(image.get('width'))
    height = float(image.get('height'))
    # Copiar imagen
    src_img = IMAGES_ORIG / img_name
    dst_img = IMAGES_OUT / img_name
    if src_img.exists():
        shutil.copy(src_img, dst_img)
    # Crear label YOLO
    label_lines = []
    for box in image.findall('box'):
        # YOLO: class_id x_center y_center width height (normalizado)
        class_id = 0
        xtl = float(box.get('xtl'))
        ytl = float(box.get('ytl'))
        xbr = float(box.get('xbr'))
        ybr = float(box.get('ybr'))
        x_center = ((xtl + xbr) / 2) / width
        y_center = ((ytl + ybr) / 2) / height
        w = (xbr - xtl) / width
        h = (ybr - ytl) / height
        label_lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}")
    # Guardar archivo label
    label_file = LABELS_OUT / (Path(img_name).stem + '.txt')
    with open(label_file, 'w') as f:
        f.write('\n'.join(label_lines))

print(f"Conversión completada. Imágenes: {len(list(IMAGES_OUT.iterdir()))}, Labels: {len(list(LABELS_OUT.iterdir()))}")