import random
import os

record_jpg_fold_root = '/home/p/data/dataImg/11_coco_y4_enb'

ratio = 0.0
# ratio = 1
record_jpg_files = os.listdir(record_jpg_fold_root)

train_files = []
valid_files = []
datas = []
for record_file in record_jpg_files:
    record_file_path = os.path.join(record_jpg_fold_root, record_file)
    f = open(record_file_path, 'r')
    datas_temp = f.readlines()
    total_num = len(datas_temp)
    valid_datas_num = int(total_num * ratio)
    valid_datas = random.sample(datas_temp, valid_datas_num)
    datas += datas_temp # all datas
    valid_files += valid_datas # valid datas

# print(datas)
# datas = datas.split('\n')
# print(datas)
random.shuffle(datas)
# print(files)
# total_num = len(datas)
# valid_datas_num = int(total_num * 0.1)
# valid_datas = random.sample(datas, valid_datas_num)

with open(record_jpg_fold_root + '/train.txt', 'w') as ft, \
        open(record_jpg_fold_root + '/val.txt', 'w') as fv:
    for file in datas:
        if file in valid_files:
            fv.write(file)
        else:
            ft.write(file)


