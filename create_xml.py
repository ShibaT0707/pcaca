import xml.etree.ElementTree as ET

name = "カレー"
image_path = ""

#image_pathの\が\\バージョン
image_new_path = ""

file_type = ""


# 生成するXMLデータをリストで用意
original_xml_data = {
    "folder": "images",
    "filename": name + "1" + file_type,
    "path": image_path + name + "1" + file_type,
    "source": {
        "database": "Unknown"
    },
    "size": {
        "width": "800",
        "height": "800",
        "depth": "3"
    },
    "segmented": "0",
    "object": {
        "name": name,
        "pose": "Unspecified",
        "truncated": "0",
        "difficult": "0",
        "bndbox": {
            "xmin": "108",
            "ymin": "203",
            "xmax": "756",
            "ymax": "622"
        }
    }
}

num_files = 241
def create_xml_element(parent, data):
    for key, value in data.items():
        if isinstance(value, dict):
            element = ET.SubElement(parent, key)
            create_xml_element(element, value)
        else:
            element = ET.SubElement(parent, key)
            element.text = value


for i in range(num_files):
    # 新しいXMLデータをコピー
    xml_data = original_xml_data.copy()

    # 新しいファイル名とパスを生成
    new_filename = f"{name}{i + 1}.jpg"
    new_path = f"{image_new_path}{name}{i + 1}.jpg"

    # 新しいファイル名とパスをXMLデータにセット
    xml_data["filename"] = new_filename
    xml_data["path"] = new_path

    # XMLファイルを生成し保存
    root = ET.Element("annotation")
    create_xml_element(root, xml_data)

    tree = ET.ElementTree(root)
    file_name = f"{name}{i + 1}.xml"

    with open(file_name, "wb") as file:
        tree.write(file, encoding="utf-8")


