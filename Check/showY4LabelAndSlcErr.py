import torch
print(torch.cuda.get_device_name())
import numpy as np
import cv2

'''
2.读取显卡的型号名称 torch.cuda.get_device_name(0)
4.查看显卡的详细信息 torch.cuda.get_device_properties(0)
'''

'''
功能：
    挑选voc的标注是否准确
'''

fileLists = []
filePath = '/home/p/data/dataImg/11_coco_y4_local/pose01.txt'

filePathSelect = filePath.replace('.txt', 'Scl.txt')
filePathProcess = filePath.replace('.txt', 'Err.txt')
filePathDrop = filePath.replace('.txt', 'Drop.txt')
with open(filePath) as f:
    fileLists = f.readlines()
# fileLists.sort()
color = (0, 0, 0)
text = ''
font = cv2.FONT_HERSHEY_SIMPLEX
lastPos = 0

# with open(filePathSelect, 'a+') as f1, open(filePathProcess, 'a+') as f2:
# with open(filePathSelect, 'w') as f1, open(filePathProcess, 'w') as f2, open(filePathDrop, 'w') as f3:
for i in range(len(fileLists)):
    print("current / totle %d / %d" % (i, len(fileLists)))
    if i < lastPos:
        continue
    file = fileLists[i]
    imgPath = file.split('\n')[0].split(' ')[0]
    # imgPath = imgPath.replace('liyanhui/data/COCO', 'p/data/COCO').replace('liyanhui/data/selfData', 'p/data')
    print(imgPath)
    bboxes = file.split('\n')[0].split(' ')[1:]
    img = cv2.imread(imgPath)
    for box in bboxes:
        xmin, ymin, xmax, ymax, _ = box.split(',')
        # if _ == '0':
        #     color = (255, 0, 0)
        #     text = 'cat'
        # elif _ == '1':
        #     color = (0, 255, 0)
        #     text = 'dog'
        # elif _ == '2':
        #     color = (0, 0, 255)
        #     text = 'person'

        if _ == '0':
            color = (255, 0, 0)
            text = 'person'
        elif _ == '1':
            color = (0, 255, 0)
            text = 'cat'
        elif _ == '2':
            color = (0, 0, 255)
            text = 'dog'
        elif _ == '3':
            color = (0, 255, 255)
            text = 'battery'

        cv2.rectangle(img, (int(xmin), int(ymin)), (int(xmax), int(ymax)), color, 2)
        image = cv2.putText(img, text, (int(xmin) + 3, int(ymin) + 15), font, 0.7, color, 2)

    cv2.imshow('we', cv2.resize(img, None, fx=0.6, fy=0.6))
    key = cv2.waitKey(0)
    # if (key == ord('w')):
    #     f1.write(file)
    # elif (key == ord('p')):
    #     f2.write(file)
    # elif (key == ord('q') or key == 27):
    #     break
    # else:
    #     f3.write(file)
