import numpy as np
from PIL import Image

image_count = 10
name = 'カレー'
image_type = '.jpg'


pca_num = 10
angle = 30
num = 0
num_max = 12
if(image_count > 1):
    name_num = 241 * (image_count - 1)
imagename = 'images/' +  name 
road_image_url = 'images/'+ name +  str(image_count) + image_type


def pca_color_augmentation(image_array_input):
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
    rotated_image = image.rotate(angle * (num + 1))
    rotated_image_array = np.array(rotated_image, dtype=np.uint8)
    return rotated_image_array

def save_image(image_array,name_num):
    edited_image = Image.fromarray(image_array)
    edited_image.save(imagename + str(name_num + 1) + image_type)
    




# 画像の読み込み
image = Image.open(road_image_url)
horizital_image = image.transpose(Image.FLIP_LEFT_RIGHT)
horizital_image.save('images/horizital_image.jpg')


image_array = np.array(image, dtype=np.uint8)
for i in range (num_max):
    for j in range(pca_num):
        image_new =pca_color_augmentation(image_array)
        save_image(image_new,name_num)
        name_num += 1
    image_array = rotate(image,i)


horizital_image = Image.open('images/horizital_image.jpg')
horizital_imgage_array = np.array(horizital_image, dtype=np.uint8)

for i in range (num_max):
    for j in range(pca_num):
        holizital_image_new = pca_color_augmentation(horizital_imgage_array)
        save_image(holizital_image_new,name_num)
        name_num += 1
    horizital_imgage_array = rotate(horizital_image,i)




