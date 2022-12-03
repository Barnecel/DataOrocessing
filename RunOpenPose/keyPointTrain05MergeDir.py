import os
import shutil
import json


rootSrcDir = r'F:\dataShare\20221129_V2img'

rootDstDir = rootSrcDir.replace('fallImg\\01', 'fallImg\\02') + 'Merge'

os.makedirs(rootDstDir, exist_ok=True)
imgSrcPaths = []

def pickUpDigit(a1):
    digit = ''
    for i in a1:
        if ord(i) <= ord('9') and ord(i) >= ord('0'):
            digit += i
    return digit

for path, dir_list, file_list in os.walk(rootSrcDir):
    for file_name in file_list:
        imgSrcPaths.append(os.path.join(path, file_name))

imgSrcPaths.sort()

for imgSrcPath in imgSrcPaths:
    # fileDstName = imgSrcPath.split('/')[-2][0:2] + '_' + imgSrcPath.split('/')[-1]
    # fileDstName = pickUpDigit(imgSrcPath.split('/')[-2].split('_')[0]) + '_' + imgSrcPath.split('/')[-1] # 只保留前两位
    fileDstName = imgSrcPath.split('\\')[-2] + '_' + imgSrcPath.split('\\')[-1]

    fileDstPath = os.path.join(rootDstDir, fileDstName)
    if not imgSrcPath.endswith('.jpg'):
        with open(imgSrcPath, 'r') as f:
            print("json path {}".format(imgSrcPath))
            jsonData = json.load(f)
            jsonData['imagePath'] = fileDstName.split('.')[0] + '.jpg'

            with open(fileDstPath, 'w') as f:
                json.dump(jsonData, f, indent=4)
        continue

    shutil.copy(imgSrcPath, fileDstPath)

