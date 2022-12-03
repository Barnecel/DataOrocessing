import os
import random
import xml.etree.ElementTree as ET

import glob


classes = ['person', 'cat', 'dog', 'battery']
def convert_annotation(xml, list_file):
    in_file = open(os.path.join(xml), encoding='utf-8')
    tree = ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = 0 
        if obj.find('difficult')!=None:
            difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            print(cls, "------------------------------------\n")
            continue
        cls_id = classes.index(cls)
        print(cls, cls_id)
        xmlbox = obj.find('bndbox')
        b = (int(float(xmlbox.find('xmin').text)), int(float(xmlbox.find('ymin').text)), int(float(xmlbox.find('xmax').text)), int(float(xmlbox.find('ymax').text)))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))
        
if __name__ == "__main__":
    random.seed(0)

    # cocoXmlPath = '/home/p/data/VOCdevkit/VOC2007/Annotations'
    # cocoImgPath = '/home/p/data/VOCdevkit/VOC2007/JPEGImages'
    # fileWriteTxt = 'label/voc/all_cdpn_train.txt'

    # cocoXmlPath = '/home/p/data/dataXml/ownDataSlc01'
    # cocoImgPath = '/home/p/data/dataImg/ownDataSlc01'
    # fileWriteTxt = cocoImgPath + '.txt'
    #
    # cocoXmlPath = '/home/p/data/dataXml/battery_new_home'
    # cocoImgPath = '/home/p/data/dataImg/battery_new_home'
    # fileWriteTxt = cocoImgPath + '.txt'





    cocoXmlPath = '/home/p/data/dataXml/battery_new_home_noTail'
    cocoImgPath = '/home/p/data/dataImg/battery_new_home_noTail'
    fileWriteTxt = cocoImgPath + '.txt'

    # cocoXmlPath = '/home/p/data/dataXml/highSlcBattery'
    # cocoImgPath = '/home/p/data/dataImg/highSlcBattery'
    # fileWriteTxt = cocoImgPath + '.txt'

    # cocoXmlPath = '/home/p/data/dataXml/ownDataSlc01_noTail'
    # cocoImgPath = '/home/p/data/dataImg/ownDataSlc01_noTail'
    # fileWriteTxt = cocoImgPath + '.txt'

    # cocoXmlPath = '/home/p/data/dataXml/ownDataSlc02_noTail'
    # cocoImgPath = '/home/p/data/dataImg/ownDataSlc02_noTail'
    # fileWriteTxt = cocoImgPath + '.txt'

    # cocoXmlPath = '/home/p/data/dataXml/ownDataSlc03_noTail'
    # cocoImgPath = '/home/p/data/dataImg/ownDataSlc03_noTail'
    # fileWriteTxt = cocoImgPath + '.txt'

    # cocoXmlPath = '/home/p/data/dataXml/y4_train_noTail_err01'
    # cocoImgPath = '/home/p/data/dataImg/y4_train_noTail_err01'
    # fileWriteTxt = cocoImgPath + '.txt'

    cocoImgPath = '/home/p/data/dataImg/ownDataSlc01'
    cocoXmlPath = '/home/p/data/dataXml/ownDataSlc01'
    fileWriteTxt = cocoImgPath + '.txt'

    xmls = glob.glob(os.path.join(cocoXmlPath, '*.xml'))

    list_file = open(fileWriteTxt, 'w', encoding='utf-8')
    for xml in xmls:
        img = xml.replace(cocoXmlPath, cocoImgPath).replace('.xml', '.jpg')
        if not os.path.exists(img):
            print(img, ' is not exit')
            continue
        list_file.write(img)

        convert_annotation(xml, list_file)
        list_file.write('\n')
    list_file.close()

