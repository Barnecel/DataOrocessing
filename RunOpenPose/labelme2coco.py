import os
import json
import numpy as np
import glob
import shutil
from sklearn.model_selection import train_test_split
np.random.seed(41)
import cv2

#0为背景
classname_to_id = {"person": 1}

class Lableme2CoCo:

    def __init__(self, splitDir=''):
        self.images = []
        self.annotations = []
        self.categories = []
        self.img_id = 0
        self.ann_id = 0
        self.splitDir = splitDir

    def save_coco_json(self, instance, save_path):
        json.dump(instance, open(save_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)  # indent=2 更加美观显示

    # 由json文件构建COCO
    def to_coco(self, json_path_list):
        self._init_categories()
        for json_path in json_path_list:
            obj = self.read_jsonfile(json_path)
            self.images.append(self._image(obj, json_path))

            shapes = obj['shapes']
            groupIds = []
            for shape in shapes:
                groupId = shape['group_id']
                groupIds.append(groupId)
            for i in set(groupIds):
                keyPoints = [0] * 51
                keyPointNum = 0
                bbox = []

                for shape in shapes:
                    if i != shape['group_id']:
                        continue
                    if shape['shape_type'] == "point":
                        labelNum = int(shape['label'])
                        keyPoints[labelNum * 3 + 0] = int(shape['points'][0][0] + 0.5)
                        keyPoints[labelNum * 3 + 1] = int(shape['points'][0][1] + 0.5)
                        keyPoints[labelNum * 3 + 2] = 2
                        keyPointNum += 1
                    if shape['shape_type'] == 'rectangle':
                        x0, y0, x1, y1 = shape['points'][0][0], shape['points'][0][1], \
                                         shape['points'][1][0], shape['points'][1][1]
                        xmin = min(x0, x1)
                        ymin = min(y0, y1)
                        xmax = max(x0, x1)
                        ymax = max(y0, y1)

                        bbox = [xmin, ymin, xmax - xmin, ymax - ymin]

                annotation = self._annotation(bbox, keyPoints, keyPointNum)
                self.annotations.append(annotation)
                self.ann_id += 1
            self.img_id += 1

            # for shape in shapes:
            #     label = shape['label']
            #     if label != 'person':
            #         continue
            #
            #     annotation = self._annotation(shape)
            #     self.annotations.append(annotation)
            #     self.ann_id += 1
            # self.img_id += 1
        instance = {}
        instance['info'] = 'spytensor created'
        instance['license'] = ['license']
        instance['images'] = self.images
        instance['annotations'] = self.annotations
        instance['categories'] = self.categories
        return instance

    # 构建类别
    def _init_categories(self):
        for k, v in classname_to_id.items():
            category = {}
            category['id'] = v
            category['name'] = k
            self.categories.append(category)

    # 构建COCO的image字段
    def _image(self, obj, jsonPath):
        image = {}
        from labelme import utils
        # img_x = utils.img_b64_to_arr(obj['imageData'])
        # h, w = img_x.shape[:-1]
        jpgPath = jsonPath.replace('.json', '.jpg')
        jpgData = cv2.imread(jpgPath)
        h, w, _ = jpgData.shape

        image['height'] = h
        image['width'] = w
        image['id'] = self.img_id

        # image['file_name'] = os.path.basename(jsonPath).replace(".json", ".jpg")
        image['file_name'] = jpgPath.split(self.splitDir)[-1]

        return image

    # 构建COCO的annotation字段
    def _annotation(self, bbox, keyPoints, keyNum):
        annotation = {}

        annotation['id'] = self.ann_id
        annotation['image_id'] = self.img_id
        annotation['category_id'] = 1
        # annotation['segmentation'] = [np.asarray(points).flatten().tolist()]
        annotation['segmentation'] = []
        annotation['bbox'] = bbox
        annotation['iscrowd'] = 0
        annotation['area'] = bbox[2] * bbox[3]
        annotation['keypoints'] = keyPoints
        annotation['num_keypoints'] = keyNum

        return annotation

    # 读取json文件，返回一个json对象
    def read_jsonfile(self, path):
        with open(path, "r", encoding='utf-8') as f:
            return json.load(f)

    # COCO的格式： [x1,y1,w,h] 对应COCO的bbox格式
    def _get_box(self, points):
        min_x = min_y = np.inf
        max_x = max_y = 0
        for x, y in points:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        return [min_x, min_y, max_x - min_x, max_y - min_y]


if __name__ == '__main__':
    labelme_path = "/home/p/data/nfsdir/00labelMePoint/fallImg/01childrenMergeResize"


    jsonName = labelme_path.split('/')[-1]
    saved_coco_path = "./selfCocoData"

    #####################################
    # 这个一定要注意
    # 为了方便合入coco数据， 定义截断文件的文件夹与文件名字
    splitDirFlag = '00labelMePoint/'
    ######################################

    # 创建文件
    if not os.path.exists("%scoco/annotations/"%saved_coco_path):
        os.makedirs("%scoco/annotations/"%saved_coco_path)
    if not os.path.exists("%scoco/images/train2017/"%saved_coco_path):
        os.makedirs("%scoco/images/train2017"%saved_coco_path)
    if not os.path.exists("%scoco/images/val2017/"%saved_coco_path):
        os.makedirs("%scoco/images/val2017"%saved_coco_path)
    # 获取images目录下所有的joson文件列表
    json_list_path = glob.glob(labelme_path + "/*.json")
    # 数据划分,这里没有区分val2017和tran2017目录，所有图片都放在images目录下
    # train_path, val_path = train_test_split(json_list_path, test_size=0.12)
    train_path, val_path = json_list_path, ''
    print("train_n:", len(train_path), 'val_n:', len(val_path))

    # 把训练集转化为COCO的json格式
    l2c_train = Lableme2CoCo(splitDirFlag)
    train_instance = l2c_train.to_coco(train_path)
    l2c_train.save_coco_json(train_instance, '%scoco/annotations/%s.json'%(saved_coco_path, jsonName))

    # # 把验证集转化为COCO的json格式
    # l2c_val = Lableme2CoCo()
    # val_instance = l2c_val.to_coco(val_path)
    # l2c_val.save_coco_json(val_instance, '%scoco/annotations/instances_val2017.json'%saved_coco_path)


    # 分离出用于训练的数据集与测试集
    # for file in train_path:
    #     shutil.copy(file.replace("json","jpg"),"%scoco/images/train2017/"%saved_coco_path)
    # for file in val_path:
    #     shutil.copy(file.replace("json","jpg"),"%scoco/images/val2017/"%saved_coco_path)

