import cv2
import shutil
import os
import glob

imgSrcDir = r'C:\Users\Enabot\Desktop\CGH\label\origin\valid02_Err_slc_block_block'
imgRstDir = imgSrcDir + 'Rst'

imgErrDir = imgSrcDir + 'Err'

imgRstPaths = glob.glob(os.path.join(imgRstDir, '*.jpg'))
imgRstPaths.sort()

showRate = 0.7
imgCount = 0
while imgCount < len(imgRstPaths):
    imgRstPath = imgRstPaths[imgCount]
    imgRstData = cv2.imread(imgRstPath)
    imgRstShowData = cv2.resize(imgRstData, None, fx=showRate, fy=showRate)
    cv2.imshow('result', imgRstShowData)
    key = cv2.waitKey(0) & 0xff
    if key == ord('e'):
        imgSrcPath = imgRstPath.replace(imgRstDir, imgSrcDir).replace('_0.jpg', '.jpg')\
            .replace('_1.jpg', '.jpg').replace('_2.jpg', '.jpg').replace('_3.jpg', '.jpg')\
            .replace('_4.jpg', '.jpg').replace('_5.jpg', '.jpg').replace('_6.jpg', '.jpg')\
            .replace('_7.jpg', '.jpg')
        jsonSrcPath = imgSrcPath.replace('.jpg', '.json')

        imgErrPath = imgSrcPath.replace(imgSrcDir, imgErrDir)
        jsonErrPath = jsonSrcPath.replace(imgSrcDir, imgErrDir)

        imgErrDir_, _ = os.path.split(jsonErrPath)
        os.makedirs(imgErrDir_, exist_ok=True)

        # shutil.copy(imgSrcPath, imgErrPath)
        # shutil.copy(jsonSrcPath, jsonErrPath)
        try:
            shutil.move(imgSrcPath, imgErrDir_)
            shutil.move(jsonSrcPath, imgErrDir_)
        except:
            print("err path ", imgSrcPath)
            pass

        imgCount += 1

    elif key == ord('j'):
        showRate += 0.05
        if showRate > 2:
            showRate = 0.05
    elif key == ord('m'):
        showRate -= 0.05
        if showRate < 0.1:
            showRate = 0.1
    elif key == ord('z'):
        imgCount -= 1
        if imgCount < 0:
            imgCount = 0
    else:
        imgCount += 1



