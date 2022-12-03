import json
import os
import glob

cocoJsonPath = '/home/p/data/COCO/annotations_14_17/person_keypoints_train2017.json'

jsonDir = '/home/p/code/miqi/prepare_detection_dataset/selfCocoDatacoco/annotations'
jsonFiles = glob.glob(os.path.join(jsonDir, '*.json'))
# jsonFiles = [jsonFile for jsonFile in jsonFiles if jsonFile.endswith('.json')]

# 读取json文件，返回一个json对象
def read_jsonfile(path):
    with open(path, "r", encoding='utf-8') as f:
        return json.load(f)

cocoJsonData = read_jsonfile(cocoJsonPath)
isCoco = 1 # 是否加入cooc的数据
def merge_JsonFiles(cocoJsonData, filename):
    baseImgCount = 0
    baseAnnCount = 0

    if not isCoco:
        cocoJsonData['images'] = []
        cocoJsonData['annotations'] = []
    else:
        for imgInfo in cocoJsonData['images']:
            imgInfo['id'] += baseImgCount

        ###############################################################
        baseImgCountMax = 0
        baseAnnCountMax = 0
        for AnnInfo in cocoJsonData['annotations']:
            AnnInfo['id'] += baseAnnCount
            if AnnInfo['id'] > baseAnnCountMax:
                baseAnnCountMax = AnnInfo['id']

            AnnInfo['image_id'] += baseImgCount
            if AnnInfo['image_id'] > baseImgCountMax:
                baseImgCountMax = AnnInfo['image_id']
        # 更新最大图片标号
        baseImgCount = baseImgCountMax
        baseAnnCount = baseAnnCountMax
    print('%s dada after baseImgCount:%d, baseAnnCount:%d' % ("coco", baseImgCount, baseAnnCount))

    for f1 in filename:
        with open(f1, 'r') as infile:
            otherJsonData = json.load(infile)
            for imgInfo in otherJsonData['images']:
                imgInfo['id'] += baseImgCount
                cocoJsonData['images'].append(imgInfo)

            ###############################################################
            baseImgCountMax = 0
            baseAnnCountMax = 0
            for AnnInfo in otherJsonData['annotations']:
                AnnInfo['id'] += baseAnnCount
                if AnnInfo['id'] > baseAnnCountMax:
                    baseAnnCountMax = AnnInfo['id']

                AnnInfo['image_id'] += baseImgCount
                if AnnInfo['image_id'] > baseImgCountMax:
                    baseImgCountMax = AnnInfo['image_id']

                cocoJsonData['annotations'].append(AnnInfo)
            # 更新最大图片标号
            baseImgCount = baseImgCountMax
            baseAnnCount = baseAnnCountMax
            print('%s dada after baseImgCount:%d, baseAnnCount:%d' % (f1, baseImgCount, baseAnnCount))

    # with open(os.path.join(jsonDir, 'counseling3.json'), 'w') as output_file:
    json.dump(cocoJsonData, open(os.path.join(jsonDir, 'counseling3.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # json.dump(result, output_file)

merge_JsonFiles(cocoJsonData, jsonFiles)






