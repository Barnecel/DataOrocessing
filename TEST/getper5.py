import shutil
import os
def ImageAllPath(pathFile):
    ImagePath_list = os.listdir(pathFile)
    print(len(ImagePath_list))
    return ImagePath_list
def ImageFor():
    # 遍历当前路径下所有文件
    pathFile = r"F:\dataShare\data_set"
    des=pathFile+"per5_1"
    n=0
    if os.path.exists(des):
        print("gonna makedir")
    else:os.makedirs(des)
    ImagePath_list = ImageAllPath(pathFile)
    print(ImagePath_list)

    for index in range(len(ImagePath_list[::5])):
        path=pathFile + '\\' + ImagePath_list[::5][index]
        print("要被复制的全文件路径全名:", path)
        if os.path.exists(path):
            shutil.copy(path, des)
            n+=1
    print("已提取",n,"个文件")


if __name__ == '__main__':
    ImageFor()

