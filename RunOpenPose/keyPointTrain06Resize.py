import json
import os
import glob
import base64
import cv2
import random

######################下面为标注遮挡点##################################################3

imgSrcDir = '/home/p/data/nfsdir/00labelMePoint/fallImg/01childrenMerge'
imgDstDir = imgSrcDir + 'Resize'


######################上面为标注遮挡点##################################################3


################下面为删除遮挡点###########################################

# imgSrcDir = '/home/p/data/nfsdir/00keyPoint/02pose_annotation/05poseSelfMergeTrain'
# imgDstDir = '/home/p/data/nfsdir/00keyPoint/02pose_annotation/06FallImgTrainNoHide'
#
# imgSrcDir = '/home/p/data/nfsdir/00keyPoint/03sofaErr01/05poseSelfMergeTrain'
# imgDstDir = '/home/p/data/nfsdir/00keyPoint/03sofaErr01/06FallImgSofaNoHide'
#
# imgSrcDir = '/home/p/data/nfsdir/00keyPoint/04home/05homeDengYu'
# imgDstDir = '/home/p/data/nfsdir/00keyPoint/04home/06homeDengYuNoHide'
#
# imgSrcDir = '/home/p/data/nfsdir/00keyPoint/04home/05homeMrDing'
# imgDstDir = '/home/p/data/nfsdir/00keyPoint/04home/06homeMrDingNoHide'
#
# imgSrcDir = '/home/p/data/nfsdir/00keyPoint/04home/05homeMrKou'
# imgDstDir = '/home/p/data/nfsdir/00keyPoint/04home/06homeMrKouNoHide'
#
# imgSrcDir = '/home/p/data/nfsdir/00keyPoint/04home/05homeTag'
# imgDstDir = '/home/p/data/nfsdir/00keyPoint/04home/06homeTagNoHide'
#
# imgSrcDir = '/home/p/data/nfsdir/00keyPoint/04home/05homeYijia'
# imgDstDir = '/home/p/data/nfsdir/00keyPoint/04home/06homeYijiaNoHide'
#
# imgSrcDir = '/home/p/data/nfsdir/00keyPoint/04home/05MrMe'
# imgDstDir = '/home/p/data/nfsdir/00keyPoint/04home/06MrMeNoHide'
#
# imgSrcDir = '/home/p/data/nfsdir/00keyPoint/04home/05MrsMe'
# imgDstDir = '/home/p/data/nfsdir/00keyPoint/04home/06MrsMeNoHide'


################上面为删除遮挡点###########################################


os.makedirs(imgDstDir, exist_ok=True)
imgSrcPaths = glob.glob(os.path.join(imgSrcDir, '*.jpg'))


for imgSrcPath in imgSrcPaths:
    resizeRate = random.uniform(0.35, 0.45)  # (1080 * 1920) -> (378, 672)(486 * 864)

    imgSrcName = imgSrcPath.split('/')[-1]
    jsonSrcPath = imgSrcPath.replace('.jpg', '.json')

    imgDstPath = imgSrcPath.replace(imgSrcDir, imgDstDir)
    jpgSrcData = cv2.imread(imgSrcPath)
    jpgDstData = cv2.resize(jpgSrcData, None, fx=resizeRate, fy=resizeRate)
    dstH, dstW, _ = jpgDstData.shape

    cv2.imwrite(imgDstPath, jpgDstData)

    with open(jsonSrcPath, 'r') as f:

        jsonData = json.load(f)
        jsonData["imageHeight"] = dstH
        jsonData["imageWidth"] = dstW

        jsonData["imagePath"] = imgSrcName
        with open(imgDstPath, "rb") as image_file:
            jpgData = base64.b64encode(image_file.read())
            jsonData["imageData"] = str(jpgData).replace('b\'', "").replace('\'', '')


        for labelMeshape in jsonData['shapes']:
            if labelMeshape['shape_type'] == 'rectangle':
                labelMeshape['points'][0][0] *= resizeRate
                labelMeshape['points'][0][1] *= resizeRate
                labelMeshape['points'][1][0] *= resizeRate
                labelMeshape['points'][1][1] *= resizeRate

            if labelMeshape['shape_type'] == 'point':
                labelMeshape['points'][0][0] *= resizeRate
                labelMeshape['points'][0][1] *= resizeRate
        with open(imgDstPath.replace('.jpg', '.json'), 'w') as f:
            json.dump(jsonData, f, indent=4)

