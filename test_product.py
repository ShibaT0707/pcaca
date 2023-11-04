import os
import re
import numpy as np
from PIL import Image
import xml.etree.ElementTree as ET

# 画像ファイルが保存されているディレクトリのパス
image_directory = 'images'
angle = 30
pca_num = 10
angle_num_max = 12
image_train_path = "images/train_imgages/"
image_val_path = "images/val_images/"
width = 0
height = 0
original_xml_data = {
    "folder": "train",
    "filename": "カレー.jpeg",
    "path": r'C:\Users\2210142\Desktop\datasets\images\train\カレー.jpeg',
    "source": {
        "database": "Unknown"
    },
    "size": {
        "width": "1240",
        "height": "827",
        "depth": "3"
    },
    "segmented": "0",
    "object": {
        "name": "カレー",
        "pose": "Unspecified",
        "truncated": "0",
        "difficult": "0",
        "bndbox": {
            "xmin": "151",
            "ymin": "214",
            "xmax": "1144",
            "ymax": "679"
        }
    }
}
def create_xml_element(parent, data):
    for key, value in data.items():
        if isinstance(value, dict):
            element = ET.SubElement(parent, key)
            create_xml_element(element, value)
        else:
            element = ET.SubElement(parent, key)
            element.text = value

def get_file_name():
    # ディレクトリ内のファイルをリストアップ
    files = os.listdir(image_directory)

    # 画像ファイルのリストをフィルタリング
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]

    # 画像ファイルの名前を表示
    for image_file in image_files:
        images_name.append(image_file)

    # ファイル名を数値としてソート
    sorted_image_files = sorted(image_files, key=lambda x: int(re.search(r'\d+', x).group(0)))
    print(sorted_image_files)
    # ソートされたファイル名を表示
    for image_file in sorted_image_files:
        images_name_sorted.append(image_file)
        # 数字より前の文字列のみを抽出
        images_name_only.append(re.search(r'\D+', image_file).group(0))
        images_num.append(int(re.search(r'\d+', image_file).group(0)))

def image_change_light(image_array_input):
    assert image_array_input.ndim == 3 and image_array_input.shape[2] == 3
    assert image_array_input.dtype == np.uint8

    img = image_array_input.reshape(-1, 3).astype(np.float32)
    img = (img - np.mean(img, axis=0)) / np.std(img, axis=0)

    cov = np.cov(img, rowvar=False)
    lambd_eigen_value, p_eigen_vector = np.linalg.eig(cov)

    rand = np.random.randn(3) * 0.1
    delta = np.dot(p_eigen_vector, rand * lambd_eigen_value)
    delta = (delta * 255.0).astype(np.int32)[np.newaxis, np.newaxis, :]

    img_out = np.clip(image_array_input + delta, 0, 255).astype(np.uint8)
    return img_out

def rotate(image, num):
    image = Image.open(os.path.join(image_directory, image))
    rotated_image = image.rotate(angle * (num + 1))
    rotated_image_array = np.array(rotated_image, dtype=np.uint8)
    return rotated_image_array

def save_image(image_array, num, i):
    edited_image = Image.fromarray(image_array)
    if int(images_num[i]) > 7:
        edited_image.save(os.path.join("val_images", f"{images_name_only[i]}{num + 1}.jpg"))

         # 新しいXMLデータをコピー
        xml_data = original_xml_data.copy()

        # 新しいファイル名とパスを生成
        new_filename = f"{images_name_only[i]}{num + 1}.jpg"
        new_path = f"{image_val_path}{images_name_only[i]}{num + 1}.jpg"

        # 新しいファイル名とパスをXMLデータにセット
        xml_data["filename"] = new_filename
        xml_data["path"] = new_path
        xml_data["size"]["width"] = str(edited_image.size[0])
        xml_data["size"]["height"] = str(edited_image.size[1])
        xml_data["size"]["depth"] = str(len(edited_image.getbands()))
        xml_data["object"]["bndbox"]["xmin"] = str(0)
        xml_data["object"]["bndbox"]["ymin"] = str(0)
        xml_data["object"]["bndbox"]["xmax"] = str(edited_image.size[0])
        xml_data["object"]["bndbox"]["ymax"] = str(edited_image.size[1])
        xml_data["object"]["name"] = images_name_only[i]
    

        # XMLファイルを生成し保存
        root = ET.Element("annotation")
        create_xml_element(root, xml_data)

        tree = ET.ElementTree(root)
        file_name = f"val_xml/{images_name_only[i]}{num + 1}.xml"

        with open(file_name, "wb") as file:
            tree.write(file, encoding="utf-8")
            
    else:
        edited_image.save(os.path.join("train_images", f"{images_name_only[i]}{num + 1}.jpg"))
        # 新しいXMLデータをコピー
        xml_data = original_xml_data.copy()

        # 新しいファイル名とパスを生成
        new_filename = f"{images_name_only[i]}{num + 1}.jpg"
        new_path = f"{image_train_path}{images_name_only[i]}{num + 1}.jpg"

        # 新しいファイル名とパスをXMLデータにセット
        xml_data["filename"] = new_filename
        xml_data["path"] = new_path
        xml_data["size"]["width"] = str(edited_image.size[0])
        xml_data["size"]["height"] = str(edited_image.size[1])
        xml_data["size"]["depth"] = str(len(edited_image.getbands()))
        xml_data["object"]["bndbox"]["xmin"] = str(0)
        xml_data["object"]["bndbox"]["ymin"] = str(0)
        xml_data["object"]["bndbox"]["xmax"] = str(edited_image.size[0])
        xml_data["object"]["bndbox"]["ymax"] = str(edited_image.size[1])
        xml_data["object"]["name"] = images_name_only[i]
    

        # XMLファイルを生成し保存
        root = ET.Element("annotation")
        create_xml_element(root, xml_data)

        tree = ET.ElementTree(root)
        file_name = f"train_xml/{images_name_only[i]}{num + 1}.xml"

        with open(file_name, "wb") as file:
            tree.write(file, encoding="utf-8")
            

images_name = []
images_name_sorted = []
images_name_only = []
images_num = []

get_file_name()

for i in range(len(images_name_only)):
    try:
        image_converted = np.array(Image.open(os.path.join(image_directory, images_name_sorted[i])), dtype=np.uint8)
    except:
        continue
    horizital_image = Image.open(os.path.join(image_directory, images_name_sorted[i])).transpose(Image.FLIP_LEFT_RIGHT)
    horizital_image.save('images/horizital_image.jpg')
    num = 1 if int(images_num[i]) == 1 else 241 * (int(images_num[i]) - 1)
    
    for j in range(2):
        for k in range(angle_num_max):
            for l in range(pca_num):
                image_lighted = image_change_light(image_converted)
                save_image(image_lighted, num, i)
                num += 1
            image_converted = rotate(images_name_sorted[i], k)
    
    image_converted = horizital_image
