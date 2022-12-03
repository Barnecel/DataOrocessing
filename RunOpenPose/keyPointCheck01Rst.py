import argparse
import json
import os
import cv2
import glob

pafsColor = [(35,  142, 35),  (66,  166, 181),
      (61,  125, 166),  (0,   127, 255),
      (219, 147, 112),  (147, 219, 112),
      (168, 168, 168),  (0,   255, 255),
      (0,   0,   0),    (159, 95,  159),
      (255, 0,   255),  (255, 255, 0),
      (66,  94,  133),  (0,   0,   0),
      (255, 0,   0),    (0,   0,   255),
      (112, 219, 219),  (0,   255, 0),
      (0,   0,   0)]

pafs = [(0, 2),   (0, 1),   (2, 4),   (1, 3),
        (4, 6),   (3, 5),   (6, 8),   (8, 10),
        (5, 7),   (7, 9),   (12, 14), (14, 16),
        (11, 13), (13, 15), (6, 12),  (5, 11)]

def createJsonData(rootDir):
    print('dir {}'.format(rootDir))
    labelMeJsons = glob.glob(os.path.join(rootDir, '*.json'))
    imgPaths = glob.glob(os.path.join(rootDir, '*.jpg'))
    if len(labelMeJsons) != len(imgPaths):
        print("\033[7;31m json num is err\033[0m")
        return -1

    print(len(labelMeJsons))

    jsonData = {}
    for labelMeJson in labelMeJsons:
        groupIdClass = []
        imgPath = ""
        with open(labelMeJson, 'r') as labelMeJsonF:
            jsonDataLabelMe = json.load(labelMeJsonF)
            jsonImg = {}
            imgPath = jsonDataLabelMe['imagePath']
            jsonImg['img_paths'] = jsonDataLabelMe['imagePath']
            jsonImg['img_height'] = jsonDataLabelMe['imageHeight']
            jsonImg['img_width'] = jsonDataLabelMe['imageWidth']
            ann = []
            for labelMeshape in jsonDataLabelMe['shapes']:
                groupIdClass.append(labelMeshape['group_id'])

            for i in set(groupIdClass):
                perLabel = {}
                keyPoints = [0] * 51
                keyPointNum = 0
                for labelMeshape in jsonDataLabelMe['shapes']:
                    if i != labelMeshape['group_id']:
                        continue
                    if labelMeshape['shape_type'] == 'rectangle':
                        x0, y0, x1, y1 = labelMeshape['points'][0][0], labelMeshape['points'][0][1], labelMeshape['points'][1][0], labelMeshape['points'][1][1],
                        if (x1 - x0 < 0 or y1 - y0 < 0):
                            bbox = [x1, y1, x0 - x1, y0 -y1]
                        else:
                            bbox = [x0, y0, x1 - x0, y1 - y0]

                        perLabel['bbox'] = bbox

                    if labelMeshape['shape_type'] == 'point':
                        labelId = int(labelMeshape['label'])
                        if labelMeshape['points'][0][0] != 0:
                            keyPoints[labelId * 3 + 2] = 1
                        else:
                            keyPoints[labelId * 3 + 2] = 0
                            continue
                        keyPoints[labelId * 3 + 0] = labelMeshape['points'][0][0]
                        keyPoints[labelId * 3 + 1] = labelMeshape['points'][0][1]
                        keyPointNum += 1
                perLabel['keypoints'] = keyPoints
                perLabel['num_keypoints'] = keyPointNum
                ann.append(perLabel)
            jsonImg['annotations'] = ann

        jsonData[str(imgPath)] = jsonImg
    return jsonData

def prepare_yunce_annotations(jsonData, net_input_size, prepared_annotations, trainPath, errPaths):
    for _, data in jsonData.items():

        imgName = data['img_paths']
        annCount = 0
        saveName = imgName
        for annotation in data['annotations']:
            ###################以下为调试信息########################################
            saveName = "%s_%d.jpg" % (imgName.split('.')[0], annCount)
            annCount += 1
            imgPath = os.path.join(trainPath, imgName)
            print("img path ", imgPath)
            imgData = cv2.imread(imgPath)

            x0, y0 = int(annotation['bbox'][0]), int(annotation['bbox'][1])
            x1, y1 = int(annotation['bbox'][0] + annotation['bbox'][2]), int(annotation['bbox'][1] + annotation['bbox'][3])
            cv2.rectangle(imgData, (x0, y0), (x1, y1), (0, 0, 255), 2)

            ###################以上为调试信息########################################

            if (annotation['num_keypoints'] < 4):
                imgErrs.append(imgPath)
                continue
            if (max(annotation['bbox'][2], annotation['bbox'][3]) < 0):
                print("imgName{}".format(imgName))
                exit()

            keypoints = []
            for i in range(len(annotation['keypoints']) // 3):
                keypoint = [annotation['keypoints'][i * 3], annotation['keypoints'][i * 3 + 1], 2, i]
                if annotation['keypoints'][i * 3 + 2] == 1:
                    keypoint[2] = 0
                elif annotation['keypoints'][i * 3 + 2] == 2:
                    keypoint[2] = 1
                keypoints.append(keypoint)
            ###################以下为调试信息########################################
            # 输出节点
            for keypoint in keypoints:
                colour = (0 ,0 , 0)
                if keypoint[2] == 2:
                    continue
                elif keypoint[2] == 1:
                    colour = (0, 0, 255)
                elif keypoint[2] == 0:
                    colour = (0, 255, 255)
                cv2.circle(imgData, (int(keypoint[0]), int(keypoint[1])), 1, colour, 2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(imgData, str(int(keypoint[3])), (int(keypoint[0]), int(keypoint[1])), font, 0.5, (0, 255, 0), 1)

            # 输出关节对
            for i in range(len(pafs)):
                paf = pafs[i]
                if keypoints[paf[0]][2] == 2 or keypoints[paf[1]][2] == 2:
                    continue
                cv2.line(imgData, (int(keypoints[paf[0]][0]), int(keypoints[paf[0]][1])),
                         (int(keypoints[paf[1]][0]), int(keypoints[paf[1]][1])), pafsColor[i], 3)

            ###################以上为调试信息########################################
            prepared_other_annotations = []
            for other_annotation in data['annotations']:
                if other_annotation == annotation:
                    continue

                prepared_other_annotation = {
                    'objpos': [other_annotation['bbox'][0] + other_annotation['bbox'][2] / 2,
                               other_annotation['bbox'][1] + other_annotation['bbox'][3] / 2],
                    'bbox': other_annotation['bbox'],
                    # 'segment_area': other_annotation['area'],
                    'scale_provided': other_annotation['bbox'][3] / net_input_size,
                    'num_keypoints': other_annotation['num_keypoints']
                }

                keypoints = []
                for i in range(len(other_annotation['keypoints']) // 3):
                    keypoint = [other_annotation['keypoints'][i * 3], other_annotation['keypoints'][i * 3 + 1], 2, i]
                    if other_annotation['keypoints'][i * 3 + 2] == 1:
                        keypoint[2] = 0
                    elif other_annotation['keypoints'][i * 3 + 2] == 2:
                        keypoint[2] = 1
                    keypoints.append(keypoint)
                prepared_other_annotation['keypoints'] = keypoints
                prepared_other_annotations.append(prepared_other_annotation)

            ###################以下为调试信息########################################
            for prepared_other_annotation in prepared_other_annotations:
                keypoints = prepared_other_annotation['keypoints']

                x0, y0 = int(prepared_other_annotation['bbox'][0]), int(prepared_other_annotation['bbox'][1])
                x1, y1 = int(prepared_other_annotation['bbox'][0] + prepared_other_annotation['bbox'][2]), int(
                    prepared_other_annotation['bbox'][1] + prepared_other_annotation['bbox'][3])
                cv2.rectangle(imgData, (x0, y0), (x1, y1), (0, 0, 255), 2)

                # for keypoint in keypoints:
                #     colour = (0 ,0 , 0)
                #     if keypoint[2] == 2:
                #         continue
                #     elif keypoint[2] == 1:
                #         colour = (0, 0, 255)
                #     elif keypoint[2] == 0:
                #         colour = (0, 255, 255)
                #     cv2.circle(imgData, (int(keypoint[0]), int(keypoint[1])), 1, colour, 2)
                #     font = cv2.FONT_HERSHEY_SIMPLEX
                #     cv2.putText(imgData, str(int(keypoint[3])), (int(keypoint[0]), int(keypoint[1])), font, 0.5,
                #                 (0, 255, 0), 1)
                # # 输出关节对
                # for i in range(len(pafs)):
                #     paf = pafs[i]
                #     if keypoints[paf[0]][2] == 2 or keypoints[paf[1]][2] == 2:
                #         continue
                #     cv2.line(imgData, (int(keypoints[paf[0]][0]), int(keypoints[paf[0]][1])),
                #              (int(keypoints[paf[1]][0]), int(keypoints[paf[1]][1])), pafsColor[i], 3)
            if 0: # show
                imgDataShow = cv2.resize(imgData, None, fx=0.8, fy=0.8)
                cv2.imshow('as2', imgDataShow)
                key = cv2.waitKey(0) & 0xff

            else: # write
                resultsDir = trainPath.split('/')[-1] + 'Rst'

                os.makedirs(resultsDir, exist_ok=True)
                resultsPath = os.path.join(resultsDir, saveName)

                cv2.imwrite(resultsPath, imgData)

            ###################以上为调试信息########################################


if __name__ == '__main__':

    trainPath = '/home/p/data/nfsdir/00labelMePoint/fallImg/04home/05homeXiaoShi'

    print('dir {}'.format(trainPath))

    parser = argparse.ArgumentParser()
    parser.add_argument('--net-input-size', type=int, default=368, help='network input size')
    args = parser.parse_args()
    errPaths = []
    prepared_annotations = []

    jsonData = createJsonData(trainPath)
    if jsonData == -1:
        exit()
    prepare_yunce_annotations(jsonData, args.net_input_size, prepared_annotations, trainPath, errPaths)

    '''
    设置颜色开始 ：\033[显示方式;前景色;背景色m
    '''





