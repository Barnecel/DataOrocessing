import argparse
import json
import os
import cv2
import glob
import xml.etree.ElementTree as ET
from xml.dom import minidom

def bbox2voc(imgPath, xmlDir, bboxes):
    annotation = ET.Element("annotation")
    imSrc = cv2.imread(imgPath)
    imgDir, imgName = os.path.split(imgPath)

    try:
        h, w, c = imSrc.shape
    except:
        # print(image_path, "is not exit!")
        return

    ET.SubElement(annotation, "filename", ).text = imgName

    image_size = ET.SubElement(annotation, 'size')
    ET.SubElement(image_size, 'width').text = str(w)
    ET.SubElement(image_size, 'height').text = str(h)
    ET.SubElement(image_size, 'depth').text = str(3)
    for box in bboxes:
        object = ET.SubElement(annotation, "object")

        ET.SubElement(object, 'name').text = str(box[4])
        ET.SubElement(object, 'difficult').text = str(0)

        bndbox = ET.SubElement(object, "bndbox")
        ET.SubElement(bndbox, 'xmin').text = str(box[0])
        ET.SubElement(bndbox, 'ymin').text = str(box[1])
        ET.SubElement(bndbox, 'xmax').text = str(box[2])
        ET.SubElement(bndbox, 'ymax').text = str(box[3])

    xmlstr = minidom.parseString(ET.tostring(annotation)).toprettyxml(indent="   ")

    xmlPath = imgPath.replace('.jpg', '.xml').replace(imgDir, xmlDir)
    with open(xmlPath, "w", encoding='utf-8') as f:
        f.write(xmlstr)

def pose2bboxes(imgJsonPath, xmlDir):
    print('dir {}'.format(imgJsonPath))
    labelMeJsons = glob.glob(os.path.join(imgJsonPath, '*.json'))

    for labelMeJson in labelMeJsons:
        imgPath = labelMeJson.replace('.json', '.jpg')
        bboxes = []
        with open(labelMeJson, 'r') as labelMeJsonF:
            jsonDataLabelMe = json.load(labelMeJsonF)

            for labelMeshape in jsonDataLabelMe['shapes']:
                if 'person' == labelMeshape['label']:
                    x0, y0, x1, y1 = labelMeshape['points'][0][0], labelMeshape['points'][0][1], labelMeshape['points'][1][0], labelMeshape['points'][1][1],
                    if (x1 - x0 < 0 or y1 - y0 < 0):
                        bbox = [x1, y1, x0, y0]
                    else:
                        bbox = [x0, y0, x1, y1]

                    bboxes.append([int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]), 'person'])

                if 'dog' == labelMeshape['label']:
                    x0, y0, x1, y1 = labelMeshape['points'][0][0], labelMeshape['points'][0][1], \
                                     labelMeshape['points'][1][0], labelMeshape['points'][1][1],
                    if (x1 - x0 < 0 or y1 - y0 < 0):
                        bbox = [x1, y1, x0, y0]
                    else:
                        bbox = [x0, y0, x1, y1]

                    bboxes.append([int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]), 'dog'])
                if 'cat' == labelMeshape['label']:
                    x0, y0, x1, y1 = labelMeshape['points'][0][0], labelMeshape['points'][0][1], \
                                     labelMeshape['points'][1][0], labelMeshape['points'][1][1],
                    if (x1 - x0 < 0 or y1 - y0 < 0):
                        bbox = [x1, y1, x0, y0]
                    else:
                        bbox = [x0, y0, x1, y1]

                    bboxes.append([int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]), 'cat'])
                if 'battery' == labelMeshape['label']:
                    x0, y0, x1, y1 = labelMeshape['points'][0][0], labelMeshape['points'][0][1], \
                                     labelMeshape['points'][1][0], labelMeshape['points'][1][1],
                    if (x1 - x0 < 0 or y1 - y0 < 0):
                        bbox = [x1, y1, x0, y0]
                    else:
                        bbox = [x0, y0, x1, y1]

                    bboxes.append([int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]), 'battery'])
        bbox2voc(imgPath, xmlDir, bboxes)

if __name__ == '__main__':
    imgJsonPath =r'C:\Users\Enabot\Desktop\test_json2xml'
    xmlDir = imgJsonPath + 'Xml'
    os.makedirs(xmlDir, exist_ok=True)

    pose2bboxes(imgJsonPath, xmlDir)

    '''
    设置颜色开始 ：\033[显示方式;前景色;背景色m
    '''





