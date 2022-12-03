


import os
import glob
import shutil

imgDir1 = r'C:\Users\Enabot\Desktop\CGH\Selection\20221129_Selecte_xml' #xml
imgDir2 = r'C:\Users\Enabot\Desktop\CGH\Selection\20221129_Selected' #jpg文件路径

imgDstDir = imgDir1+'_dst'
os.makedirs(imgDstDir, exist_ok=True)

list1 = glob.glob(os.path.join(imgDir1, '*.xml'))
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

