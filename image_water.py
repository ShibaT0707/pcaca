import os
import re
import numpy as np
from PIL import Image

# 画像ファイルが保存されているディレクトリのパス
image_directory = 'images'
images_name = []
images_name_sorted = []
images_name_only = []
images_num = []
angle = 30
image_name = ""
pca_num = 10
image_converted=""
num = 1
angle_num = 0
angle_num_max = 12
def get_file_name():

    # ディレクトリ内のファイルをリストアップ
    files = os.listdir(image_directory)

    # 画像ファイルのリストをフィルタリング
    image_files = [f for f in files if f.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp','.JPG'))]

    # 画像ファイルの名前を表示
    for image_file in image_files:
        images_name.append(image_file)


    # ファイル名を数値としてソート
    sorted_image_files = sorted(images_name, key=lambda x: int(re.search(r'\d+', x).group(0)))

    # ソートされたファイル名を表示
    for image_file in sorted_image_files:
        
        images_name_sorted.append(image_file)
        #数字より前の文字列のみを抽出
        images_name_only.append(re.search(r'\D+', image_file).group(0))
        images_num.append(int(re.search(r'\d+', image_file).group(0)))


def image_chenge_light(image_array_input):
    assert image_array_input.ndim == 3 and image_array_input.shape[2] == 3
    assert image_array_input.dtype == np.uint8

    img = image_array_input.reshape(-1, 3).astype(np.float32)
    img = (img - np.mean(img, axis=0)) / np.std(img, axis=0)

    cov = np.cov(img, rowvar=False)
    lambd_eigen_value, p_eigen_vector = np.linalg.eig(cov)

    rand = np.random.randn(3) * 0.1
    delta = np.dot(p_eigen_vector, rand*lambd_eigen_value)
    delta = (delta * 255.0).astype(np.int32)[np.newaxis, np.newaxis, :]

    img_out = np.clip(image_array_input + delta, 0, 255).astype(np.uint8)
    return img_out

def rotate(image,num):
    image = Image.open("images/" + image)
    rotated_image = image.rotate(angle * (num + 1))
    rotated_image_array = np.array(rotated_image, dtype=np.uint8)
    return rotated_image_array
    
def holigital(i):
    image_converted = np.array(Image.open("images/" + images_name_sorted[i]), dtype=np.uint8)
    image = Image.fromarray(image_converted)
    horizital_image = image.transpose(Image.FLIP_LEFT_RIGHT)
    return np.array(horizital_image, dtype=np.uint8)

def save_image(image_array,num,i):
    edited_image = Image.fromarray(image_array)
    if (i >= 7):
        edited_image.save("val_images/"+images_name_only[i] + str(num + 1) + '.jpg')
    else:
        edited_image.save("train_images/"+images_name_only[i] + str(num + 1) + '.jpg')
    

    


get_file_name()
for i in range(len(images_name_only)):
     image_converted = np.array(Image.open("images/" + images_name_sorted[i]), dtype=np.uint8)
    
     if(int(images_num[i]) == 1):
        
        num = 1
     else:
        
        num = 241 * (int(images_num[i]) - 1)
     print(num)
     for j in range(2):
        for k in range(angle_num_max):           
            for l in range(pca_num):
                image_lighted = image_chenge_light(image_converted)
                save_image(image_lighted,num,i)
                num += 1
            image_converted = rotate(images_name_sorted[i],j)
     image_converted = holigital(i)


