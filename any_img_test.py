import os
import re
import numpy as np
from PIL import Image
import xml.etree.ElementTree as ET

image_directory = 'train_images'
text_directory = 'train_xml'
output_directory = 'train_images_combined'
output_text_directory = 'train_xml_combined'
images_name = []
images_name_sorted = []
images_name_only = []
images_num = []
class_nums = []
class_num = 0
new_width = 640
num = 12000
img_width = [0] * num
img_height = [0] * num
img_width2 = [0] * num
img_height2 = [0] * num
img_width3 = [0] * num
img_height3 = [0] * num
img_width4 = [0] * num
img_height4 = [0] * num
img_width5 = [0] * num
img_height5 = [0] * num
img_width6 = [0] * num
img_height6 = [0] * num

name_num = 0


max_num = 0
over_num = 0
def get_file_name():
    global file_names_without_extension
    # ディレクトリ内のファイルをリストアップ
    files = os.listdir(image_directory)

    # 画像ファイルのリストをフィルタリング
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]

    # 画像ファイルの名前を表示
    for image_file in image_files:
        images_name.append(image_file)
        
    # ファイル名を数値としてソート
    sorted_image_files = sorted(image_files, key=lambda x: int(re.search(r'\d+', x).group(0)))
    file_names_without_extension = [os.path.splitext(file_name)[0] for file_name in sorted_image_files]

    

    # ソートされたファイル名を表示
    for image_file in sorted_image_files:
        images_name_sorted.append(image_file)
        # 数字より前の文字列のみを抽出
        images_name_only.append(re.search(r'\D+', image_file).group(0))
        
        images_num.append(int(re.search(r'\d+', image_file).group(0)))

def combine_images(i):

    global img_width, img_height, img_width2, img_height2, img_width3, img_height3, img_width4, img_height4, img_width5, img_height5, img_width6, img_height6
    global name_num
    
    images = []
    calassids = []
    count = i * 6
    data = []
    # 画像フォルダから画像を読み込む
    
    for j in range(6): 
        try: 
            image_converted = np.array(Image.open(os.path.join(image_directory, images_name_sorted[j + count])), dtype=np.uint8)
        
        

            img_path = os.path.join(image_directory, images_name_sorted[j + count])
            xml_path = os.path.join(text_directory, file_names_without_extension[j + count] + '.txt')

            aspect_ratio = new_width / image_converted.shape[1]
            new_height = int(image_converted.shape[0] * aspect_ratio)
            resized_img = Image.fromarray(image_converted).resize((new_width, new_height))
            resized_img.save(img_path)
            image_converted = np.array(resized_img, dtype=np.uint8)
            img = Image.open(img_path)
            images.append(img)
            
            with open(text_directory + '/' + file_names_without_extension[j + count] + '.txt', 'r') as file:
                line = file.readline()
                class_id_str = line.split()[0]
                class_id = int(class_id_str)
                calassids.append(class_id)
                print(calassids)
        except :
            pass

    # 画像を横に3枚、縦に2枚結合
    num_horizontal = 3
    num_vertical = 2

    # 各画像の幅と高さを取得
 
    
    img_width[i] = images[0].width
    img_height[i] = images[0].height
    img_centerx = img_width[i] / 2
    img_centery = img_height[i] / 2

    new_data1 = [calassids[0], img_centerx, img_centery, img_width[i], img_height[i]]
    data.append(new_data1)
    
    img_width2[i] = images[1].width
    img_height2[i] = images[1].height
    img_centerx2 = img_width[i] + (img_width2[i] / 2)
    img_centery2 = img_height2[i] / 2

    new_data2 = [calassids[1] if len(calassids) > 1 else 0, img_centerx2, img_centery2, img_width2[i], img_height2[i]]
    data.append(new_data2)

    img_width3[i] = images[2].width
    img_height3[i] = images[2].height
    img_centerx3 = img_width[i] + img_width2[i] + img_width3[i] / 2
    img_centery3 = img_height3[i] / 2

    new_data3 = [calassids[2] if len(calassids) > 2 else 0, img_centerx3, img_centery3, img_width3[i], img_height3[i]]
    data.append(new_data3)

    img_width4[i] = images[3].width
    img_height4[i] = images[3].height
    img_centerx4 = img_width4[i] / 2
    img_centery4 = img_height[i] + img_height4[i] / 2

    new_data4 = [calassids[3] if len(calassids) > 3 else 0, img_centerx4, img_centery4, img_width4[i], img_height4[i]]
    data.append(new_data4)
    img_width5[i] = images[4].width
    img_height5[i] = images[4].height
    img_centerx5 = img_width4[i] + img_width5[i] / 2
    img_centery5 = img_height2[i] + img_height5[i] / 2

    new_data5 = [calassids[4] if len(calassids) > 4 else 0, img_centerx5, img_centery5, img_width5[i], img_height5[i]]

    data.append(new_data5)

    img_width6[i] = images[5].width
    img_height6[i] = images[5].height
    img_centerx6 = img_width4[i] + img_width5[i] + img_width6[i] / 2
    img_centery6 = img_height3[i] + img_height6[i] / 2

    new_data6 = [calassids[5] if len(calassids) > 5 else 0, img_centerx6, img_centery6, img_width6[i], img_height6[i]]

    data.append(new_data6)

    img_widths = [img_width[i], img_width2[i], img_width3[i], img_width4[i], img_width5[i], img_width6[i]]
    img_heights = [img_height[i], img_height2[i], img_height3[i], img_height4[i], img_height5[i], img_height6[i]]

    print(data)


    # 結合された画像のサイズを計算
    total_width = img_width[i] + img_width2[i] + img_width3[i]
    total_height = img_height[i] + img_height4[i]

    # 結合された画像を作成
    combined_image = Image.new('RGB', (total_width, total_height))

    # 画像を配置
    for i in range(num_vertical):
        for j in range(num_horizontal):
            img = images[i * num_horizontal + j]
            
            combined_image.paste(img, (j * img_widths[i], i * img_heights[j]))
            

    # 一枚の画像として保存
    combined_image.save(output_directory + '/' + str(name_num) +'.jpg')
    with open(output_text_directory + '/' + str(name_num) + '.jpg', 'w') as file:
        for line in data:
            class_id, x_center, y_center, width, height = line
            yolo_line = f"{class_id} {x_center} {y_center} {width} {height}"
            file.write(yolo_line + "\n")
    name_num += 1


    


        
get_file_name()
unique_class_names = list(set(images_name_only))

for i in range(len(unique_class_names)):
     class_nums.append(class_num)
     class_num += 1

unique_class_names = list(set(images_name_only))
class_nums_for_unique_names = [class_nums[unique_class_names.index(name)] for name in images_name_only]




max_num = len(images_name_only)//6
over_num = len(images_name_only)%6

for i in range(max_num):
    combine_images(i)
    


