import cv2
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import matplotlib
import os
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def ImageAllPath(pathFile):
    ImagePath_list = os.listdir(pathFile)
    print(len(ImagePath_list))
    return ImagePath_list

def calculate(image1, image2):
    # 灰度直方图算法
    # 计算单通道的直方图的相似值
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + \
                     (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree

def classify_hist_with_split(image1, image2, size=None):
    # RGB每个通道的直方图相似度
    # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
    image1 = cv2.resize(image1, size,fx=0.5,fy=0.5)
    image2 = cv2.resize(image2, size,fx=0.5,fy=0.5)
    sub_image1 = cv2.split(image1)
    sub_image2 = cv2.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data / 3
    return sub_data

def getImageByUrl(url):
    # 根据图片url 获取图片对象
    html = requests.get(url, verify=False)
    image = Image.open(BytesIO(html.content))
    return image
def runAllImageSimilaryFun(para1, para2):
    # 均值、差值、感知哈希算法三种算法值越小，则越相似,相同图片值为0
    # 三直方图算法和单通道的直方图 0-1之间，值越大，越相似。 相同图片为1
    # t1,t2   14;19;10;  0.70;0.75
    # t1,t3   39 33 18   0.58 0.49
    # s1,s2  7 23 11     0.83 0.86  挺相似的图片
    # c1,c2  11 29 17    0.30 0.31
        # 通过imread方法直接读取物理路径
    img1 = cv2.imread(para1)
    img2 = cv2.imread(para2)


    n4 = classify_hist_with_split(img1, img2)
    print('三直方图算法相似度：', n4)
    return float(n4)






if __name__ == "__main__":
    pathFile = r"C:\Users\Enabot\Desktop\test"
    ImagePath_list = ImageAllPath(pathFile)
    print(ImagePath_list)
    for index in range(len(ImagePath_list) - 1):
        print(index)
        for index2 in range(index + 1, len(ImagePath_list)):
            print(index, "==", index2)


            path1 = pathFile + '\\' + ImagePath_list[index]
            path2 = pathFile + '\\' + ImagePath_list[index2]
            print(path1)
            print(path2)
            #判断照片是否存在
            if os.path.exists(path1)&os.path.exists(path2):
                p1 = path1
                p2 = path2
                print(p1,"Compare with",p2)
                if runAllImageSimilaryFun(p1, p2)>0.775:
                    os.remove(path2)
                    print("==============",runAllImageSimilaryFun(p1, p2))
                    index2=index2+1

                    # 停留1毫秒
                    cv2.waitKey(1)

