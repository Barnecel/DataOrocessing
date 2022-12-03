import os
import cv2

# 在一个文件下多个视频，创建图片并分解
videos_src_path = r'F:\dataShare\20221129'
videos_save_path = r'F:\dataShare\20221129'
videos = os.listdir(videos_src_path)
print(videos)
# 遍历文件夹下的视频文件
for each_video in videos:
    print('Video Name :', each_video)
    # get the name of each video, and make the directory to save frames
    # 截取视频文件的后缀，保留名称
    each_video_name = each_video.split('.', 2)[0]
    print(each_video_name)

    # 保存处理好的图片路径
    each_video_save_full_path = os.path.join(videos_save_path, each_video_name)
    print(each_video_save_full_path)
    # 创建视频同名的文件
    os.makedirs(each_video_save_full_path, exist_ok=True)

    # 获取全部视频的路径
    each_video_full_path = os.path.join(videos_src_path, each_video)
    print('path_all:' + each_video_full_path)
    # 读取全部视频
    cap = cv2.VideoCapture(each_video_full_path)
    frame_count = 0
    success = True
    while (success):
        success, frame = cap.read()
        frame_count += 1
        if frame_count % 10 == 0:
            if success:
                frame = cv2.resize(frame, (1920, 1080))
                cv2.imwrite(os.path.join(each_video_save_full_path, "%06d.jpg" % frame_count), frame)