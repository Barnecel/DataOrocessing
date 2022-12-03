import xml.etree.ElementTree as ET
from xml.dom import minidom
import cv2, os
import glob
import random


def bbox2voc(imgPath, bboxes):
    annotation = ET.Element("annotation")
    print(imgPath)
    imSrc = cv2.imread(imgPath)
    try:
        h, w, c = imSrc.shape
    except:
        return

    ET.SubElement(annotation, "filename", ).text = imgPath.split('/')[-1]

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

    xmlPath = imgPath.replace('.jpg', '.xml')
    # with open(xmlPath, "w", encoding='utf-8') as f:
    #     f.write(xmlstr)

if '__main__' == __name__:
    xmlPath = r'I:\allShare\111222\test1'
    xmls = glob.glob(os.path.join(xmlPath, '*.xml'))
    img_save = r'I:\allShare\111222\save1'
    img_bat = r'I:\allShare\111222\save'
    batterys = glob.glob(os.path.join(img_bat, '*.jpg'))
    # print(batterys)
    os.makedirs(img_save,exist_ok=True)
    for xml in xmls:
        tree = ET.parse(xml)
        root = tree.getroot()
        bboxes = []
        for obj in root.iter('object'):
            cls = obj.find('name').text
            # print(cls)
            if cls != 'battery' :
                continue
            xmlbox = obj.find('bndbox')
            box = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text),
                   int(xmlbox.find('ymax').text), cls)
            bboxes.append(box)

        boxNeeds = []
        if len(bboxes) == 0:
            continue
        if len(bboxes) > 1:
            if bboxes[0][2] - bboxes[0][0]:
                boxNeeds.append(bboxes[1])
            else:
                boxNeeds.append(bboxes[0])
        else:
            boxNeeds.append(bboxes[0])
        xml = xml.replace('.xml', '.jpg')
        bbox2voc(xml, boxNeeds)
        print(boxNeeds)
        r = random.randint(0,len(batterys)-1)
        img_b = cv2.imread(batterys[r])
        # print(r)
        print(batterys[r])
        img = cv2.imread(xml)
        # cv2.imshow('12',img)
        img_b = cv2.resize(img_b,(boxNeeds[0][2]-boxNeeds[0][0],boxNeeds[0][3]-boxNeeds[0][1]))
        # print(img_b.shape)
        img[boxNeeds[0][1]:boxNeeds[0][3],boxNeeds[0][0]:boxNeeds[0][2]] = img_b
        # print(img[boxNeeds[0][1]:boxNeeds[0][3],boxNeeds[0][0]:boxNeeds[0][2]].shape)
        # roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img,None,fx=0.5,fy=0.5)
        # cv2.imshow('1',img)
        imgsavePath = os.path.join(img_save,xml.split('\\')[-1])
        print(imgsavePath)
        cv2.imwrite(imgsavePath, img)
        cv2.waitKey(0)
        # key = cv2.waitKey(0)
        # if key == ord('q'):
        #     break
