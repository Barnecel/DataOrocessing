import cv2
import glob
import os

# q 退出
# o 下一张图片
# k 画好一张图片
# r 初始化图片

src_path = r'C:\Users\Enabot\Desktop\4Block'

dst_path = src_path + '_block'
os.makedirs(dst_path, exist_ok=True)

img_src_paths = glob.glob(os.path.join(src_path, '*.jpg'))
img_src_paths.sort()

imgRate = 1.5

# 回调函数
def MouseEvent(event, x, y, flags, param):
    global xd, yd, xu, yu, xv, yv, img_show
    img_temp = img_show.copy()
    if event == cv2.EVENT_LBUTTONDOWN:
        xd, yd = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        xu, yu = x, y
    elif event == cv2.EVENT_MOUSEMOVE and flags == 1:
        xv, yv = x, y
        cv2.rectangle(img_temp, (xd, yd), (xv, yv), (0, 0, 255), 1)
        cv2.imshow("add_block", img_temp)

    if xd != -1 and xu != -1 and not (event == cv2.EVENT_MOUSEMOVE and flags == 1):
        cv2.rectangle(img_temp, (xd, yd), (xu, yu), (0, 0, 255), 1)
        cv2.imshow("add_block", img_temp)

if __name__ == '__main__':
    xd, yd = -1, -1
    xu, yu = -1, -1
    xv, yv = -1, -1
    img_show = None

    cv2.namedWindow('add_block')
    cv2.setMouseCallback('add_block', MouseEvent)  # 窗口与回调函数绑定
    imgCount = 0
    # for img_src_path in img_src_paths:
    while imgCount < len(img_src_paths):

        img_src_path = img_src_paths[imgCount]
        print("img path : ", img_src_path)

        print(imgCount)
        img_name = os.path.basename(img_src_path)
        img_dst_path = os.path.join(dst_path, img_name)
        img_src = cv2.imread(img_src_path)
        img_write = img_src.copy()
        h, w, _ = img_src.shape
        img_size = cv2.resize(img_src, (int(w / imgRate), int(h / imgRate)))
        img_show = img_size.copy()

        while True:
            img_show_init = img_show.copy()
            if xd != -1 and xu != -1:
                cv2.rectangle(img_show_init, (xd, yd), (xu, yu), (0, 0, 255), 1)

            cv2.imshow('add_block', img_show_init)
            # cv2.imshow('add_block', img_show)
            key = cv2.waitKey(0) & 0xff

            if key == ord('q'):  # q 退出
                break
            elif key == ord('o'): # o 保存图片，跳到下一张
                cv2.imwrite(img_dst_path, img_write)
                imgCount += 1
                break
            elif key == ord('a'):
                imgCount -= 1
                break
            elif key == ord('d'): # d 不保存图片，跳到下一张
                imgCount += 1
                break
            elif key == ord('r'): # r 键恢复原图片,从新做
                img_write = img_src.copy()
                img_show = img_size.copy()
            elif key == ord('k'): # k 画好一个框，填充颜色
                color1 = img_show[yd - 1][xd - 1].tolist()  # 特别注意img的坐标取值顺序
                cv2.rectangle(img_show, (xd, yd), (xu, yu), color1, -1)
                cv2.rectangle(img_write, (int(imgRate * xd), int(imgRate * yd)), (int(imgRate * xu), int(imgRate * yu)), color1, -1)
        if key == ord('q'):
            break
    cv2.destroyAllWindows()

