#-*- coding:utf-8 -*-
'''
对图像矩阵进行矩阵分解，得到矩阵主成分，得到图像的结构单元
主要思想：每一幅图像大小为m*n的矩阵，变为m*n长度的向量，有S个图像，所以可以组成S * (m*n)的矩阵，然后进行分解成S * K的矩阵乘以K * (m*n)的矩阵，
即得到了K个(m*n)的分量，把这些当作结构单元。
'''

from PIL import Image
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt

IMAGE_SIZE = 64
# 加载图片矩阵，每个彩色图像变为RGB三通道
# RGB三通道加入图像矩阵，并水平翻转
def load_pics(pics_dir):
    pics_files = [os.path.join(pics_dir, fname) for fname in os.listdir(pics_dir)]
    imgs_arrays = []
    for img_path in pics_files:
        img = Image.open(img_path)
        img = img.resize((IMAGE_SIZE, IMAGE_SIZE))
        img_array = np.array(img, dtype = np.float64)
        img_red_array = img_array[:, :, 0]
        img_green_array = img_array[:, :, 1]
        img_blue_array = img_array[:, :, 2]
        
        imgs_arrays.append(img_red_array.flatten())
        imgs_arrays.append(img_green_array.flatten())
        imgs_arrays.append(img_blue_array.flatten())
        
        imgs_arrays.append(img_red_array[:,::-1].flatten())
        imgs_arrays.append(img_green_array[:,::-1].flatten())
        imgs_arrays.append(img_blue_array[:,::-1].flatten())
        
    imgs_arrays = np.array(imgs_arrays)
    return imgs_arrays

# 加载图片: 图片数量 * 图片像素点
imgs_arrays = load_pics(pics_dir = "pics/norm_small_pics")
print(imgs_arrays.shape)

# 标准化
scaler = StandardScaler()
scaler.fit(imgs_arrays)
imgs_arrays = scaler.transform(imgs_arrays)
print(np.mean(imgs_arrays[:, 0]), np.var(imgs_arrays[:, 0]))

# PCA降维
pca = PCA(n_components = 80)
pca.fit(imgs_arrays)
comps = pca.components_

print(np.sum(pca.explained_variance_ratio_))
print(pca.n_components_)
print(comps.shape)

for i, com in enumerate(comps):
    if i % 10 != 0:
        continue
    img_comp = com.reshape(IMAGE_SIZE, IMAGE_SIZE)
    plt.figure()
    plt.imshow(img_comp)
    plt.show()