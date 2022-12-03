import glob
import os
import shutil

rootSrcDir = r'C:\Users\Enabot\Desktop\Selections'
# rootSrcDir = '/home/ebo/data/Home/future/Untitled Folder'
imgDstDir = rootSrcDir + '_new'
os.makedirs(imgDstDir, exist_ok=True)

imgSrcPaths = []

for path, dir_list, file_list in os.walk(rootSrcDir):
    for file_name in file_list:
        imgSrcPaths.append(os.path.join(path, file_name))

imgSrcPaths.sort()

for imgSrcPath in imgSrcPaths:
    imgSrcPathKeys = imgSrcPath.split('\\')
    mergeName = imgSrcPathKeys[-2][:-10] + '_' + imgSrcPathKeys[-1]
    imgDstPath = os.path.join(imgDstDir, mergeName)

    print(imgSrcPath, imgDstPath)
    shutil.copy(imgSrcPath, imgDstPath)