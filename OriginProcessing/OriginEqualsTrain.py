


import os
import glob
import shutil
imgDir1 = r'C:\Users\Enabot\Desktop\CGH\BatteryToImageMerge' #源文件文件路径
imgDir2 = r'C:\Users\Enabot\Desktop\CGH\Selection\BatteryToImage_new_jjj_Selected' #所筛选的训练样本
imgDstDir = imgDir1+'_Suplers'

os.makedirs(imgDstDir, exist_ok=True)

list1 = glob.glob(os.path.join(imgDir1, '*.jpg'))
list2 = glob.glob(os.path.join(imgDir2, '*.jpg'))
list2 = os.listdir(imgDir2)
print(list2)
img_nojpg = []
for l in list2:
    img_nojpg.append(l[:-4])
print(img_nojpg)
i=0

for img in list1:
    img1 = img.split('\\')[-1]
    imgs = img.split('\\')[-1][:-4]
    print(img1)
    if imgs not in img_nojpg:
        imgPath1 = img
        print(imgPath1)
        imgPathDst = imgPath1.replace(imgDir1,imgDstDir)
        i+=1
        print(i,'path:',imgPathDst)
        shutil.move(imgPath1,imgDstDir)

