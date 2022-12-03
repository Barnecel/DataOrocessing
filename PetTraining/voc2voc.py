import xml.etree.ElementTree as ET
from xml.dom import minidom
import cv2, os
import glob

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
    with open(xmlPath, "w", encoding='utf-8') as f:
        f.write(xmlstr)

if '__main__' == __name__:
    xmlPath = ''
    xmls = glob.glob(os.path.join(xmlPath, '*.xml'))
    for xml in xmls:
        tree = ET.parse(xml)
        root = tree.getroot()

        bboxes = []
        for obj in root.iter('object'):
            cls = obj.find('name').text

            xmlbox = obj.find('bndbox')
            box = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text),
                   int(xmlbox.find('ymax').text), cls)

            bboxes.append(box)

        boxNeeds = []
        if len(bboxes) > 1:
            if bboxes[0][2] - bboxes[0][0]:
                boxNeeds.append(bboxes[1])
            else:
                boxNeeds.append(bboxes[0])
        else:
            boxNeeds.append(bboxes[0])
        xml = xml.replace('.xml', '.jpg')
        bbox2voc(xml, boxNeeds)


