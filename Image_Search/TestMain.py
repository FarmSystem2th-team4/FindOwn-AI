# from Test import CNNModel
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg

# root_dir = "C:\\Users\\DGU_ICE\\FindOwn\\ImageDB\\Logos"
# target_image_path = "C:\\Users\\DGU_ICE\\FindOwn\\ImageDB\\image-05.png"
# compare_image_path = "C:\\Users\\DGU_ICE\\FindOwn\\ImageDB\\KakaoTalk_20230216_133749847.png"

# cnn = CNNModel()
# cnn_similarities = cnn.compare_features(target_image_path, 'cnn_features.pkl')

# print(cnn_similarities[:10])
# image_paths = cnn_similarities[:10]

# for i in range(len(image_paths)):
#     image_paths[i] = (root_dir + '\\' + image_paths[i][0], image_paths[i][1])
# # 서브플롯 생성
# fig, ax = plt.subplots(3, 4, figsize=(20, 15))

# # 타겟 이미지 표시
# img = mpimg.imread(target_image_path)
# ax[0, 0].imshow(img)
# ax[0, 0].set_title("Target Image")

# # 나머지 이미지 표시
# for i in range(1, len(image_paths) + 1):
#     img = mpimg.imread(image_paths[i-1][0])
#     ax[i // 4, i % 4].imshow(img)
#     ax[i // 4, i % 4].set_title("Similarity: {:.8f}".format(image_paths[i-1][1]))

# # 빈 서브플롯 숨기기
# for i in range(len(image_paths) + 1, 12):
#     fig.delaxes(ax.flatten()[i])

# plt.tight_layout()
# plt.show()

from pydantic import BaseModel
import models
import cv2
import pickle
import os
import urllib.request
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.image as mpimg

# Initialize the models.
# url을 받아오는 걸로 변경 요망
################################################################################################################
target_image_path = "https://trademark.help-me.kr/images/blog/trademark-registration-all-inclusive/image-05.png"
################################################################################################################
root_dir = "C:\\Users\\DGU_ICE\\FindOwn\\ImageDB\\Logos"
#target_image_path를 url로 받아오면 아래 코드로 유사도 검사 후 결과 dict를 json으로 만들어 다시 전송
similar_results_dict = {}
with open('features_logo.pkl','rb') as f:
    load = pickle.load(f)
for image_path, array in load:
    similar_results_dict.update({image_path:0.0})

similar_model = models.Image_Search_Model(pre_extracted_features='features_logo.pkl')
efficientnet_image_list = similar_model.search_similar_images(target_image_path,len(similar_results_dict))
for image_path, accuracy in efficientnet_image_list:
    similar_results_dict[image_path] += 0.6 * accuracy
similar_results_dict = sorted(similar_results_dict.items(), key=lambda x: x[1], reverse=True)
N = 3  # Display top N images
fig, ax = plt.subplots(1, N+1, figsize=(20, 10))

# Display target image
if target_image_path.startswith('http://') or target_image_path.startswith('https://'):
    with urllib.request.urlopen(target_image_path) as url:
        img = Image.open(url).convert('RGB')
        img = np.array(img)
else:
    img = mpimg.imread(target_image_path)
ax[0].imshow(img)
ax[0].set_title("Target Image")

# Display top N similar images
for i in range(1, N+1):
    img_path, accuracy = similar_results_dict[i-1]
    if img_path.startswith('http://') or img_path.startswith('https://'):
        with urllib.request.urlopen(img_path) as url:
            img = Image.open(url)
            img = np.array(img)
    else:
        img = mpimg.imread(img_path)
    ax[i].imshow(img)
    ax[i].set_title("Similarity: {:.8f}".format(accuracy))

plt.tight_layout()
plt.show()

color_model = models.ColorSimilarityModel()
if not os.path.exists('colorHistograms_logo.pkl'):
    color_model.save_histograms(root_dir,'colorHistograms_logo.pkl')
histograms = color_model.load_histograms('colorHistograms_logo.pkl')
similarities = color_model.predict(target_image_path, histograms)
color_dicision_images = similarities

similar_results_dict = {}
for image_path, array in load:
    similar_results_dict.update({image_path:0.0})
    
for img_path, color_accuracy in color_dicision_images:
    similar_results_dict[img_path] = 0
    similar_results_dict[img_path] += 0.1 * color_accuracy
similar_results_dict = sorted(similar_results_dict.items(), key=lambda x: x[1], reverse=True)

N = 3  # Display top N images
fig, ax = plt.subplots(1, N+1, figsize=(20, 10))

# Display target image
if target_image_path.startswith('http://') or target_image_path.startswith('https://'):
    with urllib.request.urlopen(target_image_path) as url:
        img = Image.open(url).convert('RGB')
        img = np.array(img)
else:
    img = mpimg.imread(target_image_path)
ax[0].imshow(img)
ax[0].set_title("Target Image")

# Display top N similar images
for i in range(1, N+1):
    img_path, accuracy = similar_results_dict[i-1]
    if img_path.startswith('http://') or img_path.startswith('https://'):
        with urllib.request.urlopen(img_path) as url:
            img = Image.open(url)
            img = np.array(img)
    else:
        img = mpimg.imread(img_path)
    ax[i].imshow(img)
    ax[i].set_title("Similarity: {:.8f}".format(accuracy))

plt.tight_layout()
plt.show()

    
Object_model  = models.Image_Object_Detections(len(similar_results_dict))
if not os.path.exists('object_logo.pkl'):
    Object_model.create_object_detection_pkl(root_dir,'object_logo.pkl')
with open('object_logo.pkl','rb') as f:
    detection_dict = pickle.load(f)
result = Object_model.search_similar_images(target_image_path,detection_dict)


similar_results_dict = {}
for image_path, array in load:
    similar_results_dict.update({image_path:0.0})
    
for img_path, _, object_accuracy in result:
    similar_results_dict[img_path] = 0
    similar_results_dict[img_path] += 0.1 * object_accuracy
similar_results_dict = sorted(similar_results_dict.items(), key=lambda x: x[1], reverse=True)
N = 3  # Display top N images
fig, ax = plt.subplots(1, N+1, figsize=(20, 10))

# Display target image
if target_image_path.startswith('http://') or target_image_path.startswith('https://'):
    with urllib.request.urlopen(target_image_path) as url:
        img = Image.open(url).convert('RGB')
        img = np.array(img)
else:
    img = mpimg.imread(target_image_path)
ax[0].imshow(img)
ax[0].set_title("Target Image")

# Display top N similar images
for i in range(1, N+1):
    img_path, accuracy = similar_results_dict[i-1]
    if img_path.startswith('http://') or img_path.startswith('https://'):
        with urllib.request.urlopen(img_path) as url:
            img = Image.open(url)
            img = np.array(img)
    else:
        img = mpimg.imread(img_path)
    ax[i].imshow(img)
    ax[i].set_title("Similarity: {:.8f}".format(accuracy))

plt.tight_layout()
plt.show()

similar_results_dict = {}
for image_path, array in load:
    similar_results_dict.update({image_path:0.0})
    
cnn = models.CNNModel()
if not os.path.exists('cnn_features.pkl'):
    cnn.extract_features_from_dir(root_dir, 'cnn_features.pkl')
cnn_similarities = cnn.compare_features(target_image_path, 'cnn_features.pkl')
for img_path, cnn_accuracy in cnn_similarities:
    img_path = root_dir+'\\'+img_path
    similar_results_dict[img_path] = 0
    similar_results_dict[img_path] += 1.0 * cnn_accuracy
similar_results_dict = sorted(similar_results_dict.items(), key=lambda x: x[1], reverse=True)


#################################   Print Test Code  #########################################

N = 3  # Display top N images
fig, ax = plt.subplots(1, N+1, figsize=(20, 10))

# Display target image
if target_image_path.startswith('http://') or target_image_path.startswith('https://'):
    with urllib.request.urlopen(target_image_path) as url:
        img = Image.open(url).convert('RGB')
        img = np.array(img)
else:
    img = mpimg.imread(target_image_path)
ax[0].imshow(img)
ax[0].set_title("Target Image")

# Display top N similar images
for i in range(1, N+1):
    img_path, accuracy = similar_results_dict[i-1]
    if img_path.startswith('http://') or img_path.startswith('https://'):
        with urllib.request.urlopen(img_path) as url:
            img = Image.open(url)
            img = np.array(img)
    else:
        img = mpimg.imread(img_path)
    ax[i].imshow(img)
    ax[i].set_title("Similarity: {:.8f}".format(accuracy))

plt.tight_layout()
plt.show()