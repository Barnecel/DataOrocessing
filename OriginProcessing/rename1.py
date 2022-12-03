import os

path_name = r'F:\dataShare\20221129'
count = os.listdir(path_name)

count.sort(key= lambda x:int(x[:-4]))

for i in range(0, len(count)):  # 进入到文件夹内，对每个文件进行循环遍历
    j = 1  # 表示图像名称从0开始
    k = str(i + j)
    other_url = k.zfill(2)  # 总共2位，除了数字部位，其余用0填充 zfill指定字符串长度原字符串对齐，位数不足前面补0
    # os.path.join(path_name,item)表示找到每个文件的绝对路径并进行拼接操作
    # os.rename(os.path.join(path_name, count[i]), os.path.join(path_name, '220630' + other_url + '_X'))
    # os.rename(os.path.join(path_name, count[i]), os.path.join(path_name, ('220711' + other_url + '.avi')))
    os.rename(os.path.join(path_name, count[i]), os.path.join(path_name, ('221129' + other_url + '.mp4')))
    # os.rename(os.path.join(path_name, count[i]), os.path.join(path_name, ('220715' + other_url + '_air' + '.avi')))
    # os.rename(os.path.join(path_name, count[i]), os.path.join(path_name, (other_url + '.jpg')))
    # os.rename(os.path.join(path_name, count[i]), os.path.join(path_name, ('0330' + other_url + 'pm')))
    # rename(修改的目录名，修改后的目录名)
    j += 1

print("Rename_Successed")






# import glob
# import os
# import shutil
#
# imgDir = r'I:\allShare\datasets\Fall\FallImg\Dinglijie\X_right\1'
#
# imgDstDir = r'I:\allShare\datasets\Fall\FallImg\Dinglijie\X_right\1\11'
# os.makedirs(imgDstDir, exist_ok=True)
#
# imgPath1s = glob.glob(os.path.join(imgDir, '*.png'))
#
# # imgPath1s.sort()
# for imgPath1 in imgPath1s:
#     if imgPath1.endswith('.png'):
#         imgName1 = imgPath1.split('\\')[-1].split('.')[0]
#         imgDstPath1 = os.path.join(imgDstDir, imgName1) + '.jpg'
#         print(imgPath1)
#         print(imgDstPath1)
#         shutil.copy(imgPath1, imgDstPath1)

